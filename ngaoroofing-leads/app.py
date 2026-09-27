"""Flask routes for capturing and viewing individual leads."""

import math
import os
import sqlite3
from datetime import date

from flask import Flask, abort, redirect, render_template, request, url_for

from database import (
    DATABASE_PATH,
    LEAD_STATUSES,
    create_lead,
    create_follow_up,
    get_all_leads,
    get_lead_count,
    get_follow_ups_for_lead,
    get_lead_profile,
    get_leads_for_list,
    get_sales_action_queue,
    initialize_database,
    SALES_QUEUE_CATEGORIES,
    update_lead_status as update_lead_status_in_db,
)


SOURCE_OPTIONS = (
    "WhatsApp",
    "X",
    "Phone",
    "Website",
    "Referral",
    "Email",
    "Walk-in",
    "Other",
)
PROJECT_TYPE_OPTIONS = (
    "Residential",
    "Estate",
    "Hotel",
    "School",
    "Commercial",
    "Apartment",
    "Other",
)
STATUS_OPTIONS = LEAD_STATUSES
FOLLOW_UP_OPTIONS = (
    "OVERDUE",
    "DUE TODAY",
    "DUE SOON",
    "UPCOMING",
    "NO FOLLOW-UP",
)
FOLLOW_UP_METHOD_OPTIONS = (
    "Phone",
    "WhatsApp",
    "Email",
    "X",
    "Site Visit",
    "In Person",
    "Other",
)
QUEUE_EMPTY_MESSAGES = {
    "OVERDUE": "No overdue follow-ups.",
    "DUE TODAY": "No follow-ups due today.",
    "DUE SOON": "No follow-ups due in the next 7 days.",
    "NO FOLLOW-UP": "All active leads have a follow-up scheduled.",
    "UPCOMING": "No upcoming follow-ups.",
}

app = Flask(__name__)
app.config["DATABASE_PATH"] = os.environ.get(
    "NGAO_ROOFING_DATABASE",
    str(DATABASE_PATH),
)


def _is_valid_iso_date(value):
    if not value:
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def _format_display_date(value):
    if not value:
        return "Not set"
    if not _is_valid_iso_date(value):
        return value
    return date.fromisoformat(value).strftime("%B %d, %Y").replace(" 0", " ")


app.add_template_filter(_format_display_date, "display_date")


def _read_form_data():
    field_names = (
        "name",
        "phone",
        "email",
        "company",
        "source",
        "project_type",
        "location",
        "estimated_roof_area",
        "product_profile",
        "inquiry_date",
        "status",
        "notes",
        "next_action",
        "next_follow_up_date",
    )
    return {field: request.form.get(field, "").strip() for field in field_names}


def _validate_form(form):
    errors = {}

    if not form["name"]:
        errors["name"] = "Enter the lead's name."

    for field, label in (
        ("inquiry_date", "Inquiry date"),
        ("next_follow_up_date", "Next follow-up date"),
    ):
        value = form[field]
        if field == "inquiry_date" and not value:
            errors[field] = "Enter the date the inquiry was received."
        elif value and not _is_valid_iso_date(value):
            errors[field] = f"{label} must be a valid date."

    if form["status"] not in STATUS_OPTIONS:
        errors["status"] = "Choose a valid lead status."
    if form["source"] and form["source"] not in SOURCE_OPTIONS:
        errors["source"] = "Choose a source from the list."
    if form["project_type"] and form["project_type"] not in PROJECT_TYPE_OPTIONS:
        errors["project_type"] = "Choose a project type from the list."

    roof_area = None
    if form["estimated_roof_area"]:
        try:
            roof_area = float(form["estimated_roof_area"])
            if not math.isfinite(roof_area) or roof_area < 0:
                raise ValueError
        except ValueError:
            errors["estimated_roof_area"] = "Enter a non-negative roof area."

    return errors, roof_area


def _find_duplicate_leads(form):
    phone_digits = "".join(character for character in form["phone"] if character.isdigit())
    email_address = form["email"].casefold()
    if not phone_digits and not email_address:
        return []

    matches = []
    existing_leads = get_all_leads(
        include_archived=True,
        database_path=app.config["DATABASE_PATH"],
    )
    for lead in existing_leads:
        reasons = []
        existing_phone = "".join(
            character for character in (lead["phone"] or "") if character.isdigit()
        )
        existing_email = (lead["email"] or "").strip().casefold()
        if phone_digits and phone_digits == existing_phone:
            reasons.append("phone number")
        if email_address and email_address == existing_email:
            reasons.append("email address")
        if reasons:
            matches.append(
                {
                    "id": lead["id"],
                    "name": lead["name"],
                    "reasons": ", ".join(reasons),
                }
            )
    return matches


def _render_lead_profile(
    lead_id,
    follow_up_form=None,
    errors=None,
    just_saved=False,
    follow_up_logged=False,
    status_message=None,
    status_error=False,
    status_code=200,
):
    lead = get_lead_profile(
        lead_id,
        today=date.today().isoformat(),
        database_path=app.config["DATABASE_PATH"],
    )
    if lead is None:
        abort(404)

    if follow_up_form is None:
        follow_up_form = {
            "contact_date": date.today().isoformat(),
            "contact_method": "",
            "what_happened": "",
            "customer_response": "",
            "outcome": "",
            "next_action": lead["next_action"] or "",
            "next_follow_up_date": lead["next_follow_up_date"] or "",
        }

    response = render_template(
        "lead_detail.html",
        lead=lead,
        follow_ups=get_follow_ups_for_lead(
            lead_id,
            database_path=app.config["DATABASE_PATH"],
        ),
        follow_up_form=follow_up_form,
        errors=errors or {},
        follow_up_method_options=FOLLOW_UP_METHOD_OPTIONS,
        status_options=STATUS_OPTIONS,
        just_saved=just_saved,
        follow_up_logged=follow_up_logged,
        status_message=status_message,
        status_error=status_error,
    )
    if status_code == 200:
        return response
    return response, status_code


@app.get("/")
def home():
    queue = get_sales_action_queue(
        today=date.today().isoformat(),
        database_path=app.config["DATABASE_PATH"],
    )
    return render_template(
        "sales_queue.html",
        queue=queue,
        category_order=SALES_QUEUE_CATEGORIES,
        empty_messages=QUEUE_EMPTY_MESSAGES,
    )


@app.get("/leads")
def lead_list():
    search = request.args.get("q", "").strip()
    status_filter = request.args.get("status", "")
    source_filter = request.args.get("source", "")
    follow_up_filter = request.args.get("follow_up", "")
    scope = "all" if request.args.get("scope") == "all" else "active"

    if status_filter not in STATUS_OPTIONS:
        status_filter = ""
    if source_filter not in SOURCE_OPTIONS:
        source_filter = ""
    if follow_up_filter not in FOLLOW_UP_OPTIONS:
        follow_up_filter = ""

    leads = get_leads_for_list(
        search=search,
        status=status_filter,
        source=source_filter,
        follow_up=follow_up_filter,
        include_inactive=scope == "all",
        today=date.today().isoformat(),
        database_path=app.config["DATABASE_PATH"],
    )
    total_leads = get_lead_count(database_path=app.config["DATABASE_PATH"])

    return render_template(
        "leads.html",
        leads=leads,
        total_leads=total_leads,
        search=search,
        status_filter=status_filter,
        source_filter=source_filter,
        follow_up_filter=follow_up_filter,
        scope=scope,
        has_filters=bool(search or status_filter or source_filter or follow_up_filter),
        status_options=STATUS_OPTIONS,
        source_options=SOURCE_OPTIONS,
        follow_up_options=FOLLOW_UP_OPTIONS,
    )


@app.route("/leads/new", methods=["GET", "POST"])
def add_lead():
    if request.method == "GET":
        form = {"inquiry_date": date.today().isoformat(), "status": "NEW"}
        return render_template(
            "lead_form.html",
            form=form,
            errors={},
            duplicate_matches=[],
            duplicate_confirmation_missing=False,
            source_options=SOURCE_OPTIONS,
            project_type_options=PROJECT_TYPE_OPTIONS,
            status_options=STATUS_OPTIONS,
        )

    form = _read_form_data()
    form["confirm_duplicate"] = request.form.get("confirm_duplicate", "")
    errors, roof_area = _validate_form(form)
    duplicate_matches = _find_duplicate_leads(form) if not errors else []
    duplicate_confirmation_missing = bool(
        duplicate_matches and form["confirm_duplicate"] != "yes"
    )

    if errors or duplicate_confirmation_missing:
        return render_template(
            "lead_form.html",
            form=form,
            errors=errors,
            duplicate_matches=duplicate_matches,
            duplicate_confirmation_missing=duplicate_confirmation_missing,
            source_options=SOURCE_OPTIONS,
            project_type_options=PROJECT_TYPE_OPTIONS,
            status_options=STATUS_OPTIONS,
        ), 400 if errors else 200

    lead_data = {
        field: form[field] or None
        for field in (
            "name",
            "phone",
            "email",
            "company",
            "source",
            "project_type",
            "location",
            "product_profile",
            "inquiry_date",
            "status",
            "notes",
            "next_action",
            "next_follow_up_date",
        )
    }
    lead_data["estimated_roof_area"] = roof_area

    try:
        lead_id = create_lead(lead_data, database_path=app.config["DATABASE_PATH"])
    except sqlite3.Error:
        app.logger.exception("Could not save a lead to SQLite.")
        errors["form"] = "The lead could not be saved. Your entries are still here; please try again."
        return render_template(
            "lead_form.html",
            form=form,
            errors=errors,
            duplicate_matches=[],
            duplicate_confirmation_missing=False,
            source_options=SOURCE_OPTIONS,
            project_type_options=PROJECT_TYPE_OPTIONS,
            status_options=STATUS_OPTIONS,
        ), 500

    return redirect(url_for("view_lead", lead_id=lead_id, saved="1"))


@app.get("/leads/<int:lead_id>")
def view_lead(lead_id):
    return _render_lead_profile(
        lead_id,
        just_saved=request.args.get("saved") == "1",
        follow_up_logged=request.args.get("follow_up_logged") == "1",
        status_message=request.args.get("status_message") or None,
        status_error=request.args.get("status_error") == "1",
    )


@app.post("/leads/<int:lead_id>/status")
def update_lead_status(lead_id):
    lead = get_lead_profile(
        lead_id,
        today=date.today().isoformat(),
        database_path=app.config["DATABASE_PATH"],
    )
    if lead is None:
        abort(404)

    new_status = (request.form.get("status", "") or "").strip()
    if new_status not in STATUS_OPTIONS:
        return redirect(
            url_for("view_lead", lead_id=lead_id, status_error="1"),
        )

    try:
        updated = update_lead_status_in_db(
            lead_id,
            new_status,
            database_path=app.config["DATABASE_PATH"],
        )
    except ValueError:
        return redirect(
            url_for("view_lead", lead_id=lead_id, status_error="1"),
        )

    if not updated:
        abort(404)

    return redirect(
        url_for("view_lead", lead_id=lead_id, status_message="Status updated."),
    )


@app.post("/leads/<int:lead_id>/follow-ups")
def log_follow_up(lead_id):
    lead = get_lead_profile(
        lead_id,
        today=date.today().isoformat(),
        database_path=app.config["DATABASE_PATH"],
    )
    if lead is None:
        abort(404)

    form = {
        field: request.form.get(field, "").strip()
        for field in (
            "contact_date",
            "contact_method",
            "what_happened",
            "customer_response",
            "outcome",
            "next_action",
            "next_follow_up_date",
        )
    }
    errors = {}

    if not _is_valid_iso_date(form["contact_date"]):
        errors["contact_date"] = "Enter a valid contact date."
    if form["next_follow_up_date"] and not _is_valid_iso_date(form["next_follow_up_date"]):
        errors["next_follow_up_date"] = "Next follow-up date must be a valid date."
    if form["contact_method"] and form["contact_method"] not in FOLLOW_UP_METHOD_OPTIONS:
        errors["contact_method"] = "Choose a contact method from the list."

    if errors:
        return _render_lead_profile(lead_id, form, errors, status_code=400)

    follow_up_data = {
        "lead_id": lead_id,
        "contact_date": form["contact_date"],
        "contact_method": form["contact_method"] or None,
        "what_happened": form["what_happened"] or None,
        "customer_response": form["customer_response"] or None,
        "outcome": form["outcome"] or None,
        "next_action": form["next_action"] or None,
        "next_follow_up_date": form["next_follow_up_date"] or None,
    }

    try:
        create_follow_up(follow_up_data, database_path=app.config["DATABASE_PATH"])
    except sqlite3.Error:
        app.logger.exception("Could not save a follow-up to SQLite.")
        errors["form"] = "The follow-up could not be saved. Your entries are still here; please try again."
        return _render_lead_profile(lead_id, form, errors, status_code=500)

    return redirect(url_for("view_lead", lead_id=lead_id, follow_up_logged="1"))


if __name__ == "__main__":
    initialize_database(app.config["DATABASE_PATH"])
    app.run(debug=True, use_reloader=False)