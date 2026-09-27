"""Small SQLite access functions for the Ngao Roofing lead tracker."""

import sqlite3
from contextlib import closing
from datetime import date, datetime, timedelta
from pathlib import Path


PROJECT_DIRECTORY = Path(__file__).resolve().parent
DATABASE_PATH = PROJECT_DIRECTORY / "instance" / "ngaoroofing.sqlite3"
SCHEMA_PATH = PROJECT_DIRECTORY / "schema.sql"

LEAD_FIELDS = (
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
LEAD_STATUSES = (
    "NEW",
    "QUALIFIED",
    "QUOTED",
    "FOLLOW-UP",
    "SITE VISIT",
    "NEGOTIATION",
    "WON",
    "LOST",
    "DORMANT",
)
CLOSED_LEAD_STATUSES = ("WON", "LOST", "DORMANT")
ACTIVE_LEAD_STATUSES = tuple(
    status for status in LEAD_STATUSES if status not in CLOSED_LEAD_STATUSES
)
SALES_QUEUE_CATEGORIES = (
    "OVERDUE",
    "DUE TODAY",
    "DUE SOON",
    "NO FOLLOW-UP",
    "UPCOMING",
)
_ACTIVE_STATUS_SQL = ", ".join(
    f":active_status_{index}" for index in range(len(ACTIVE_LEAD_STATUSES))
)
_ACTIVE_STATUS_PARAMETERS = {
    f"active_status_{index}": status
    for index, status in enumerate(ACTIVE_LEAD_STATUSES)
}


def _timestamp_now():
    """Return a high-precision SQLite-friendly timestamp for updates."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%f")


def get_database_connection(database_path=DATABASE_PATH):
    """Open SQLite and enable foreign-key checks for this connection."""
    if database_path is None:
        database_path = DATABASE_PATH
    database_path = Path(database_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(database_path=DATABASE_PATH):
    """Create missing tables without replacing any existing tables or data."""
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with closing(get_database_connection(database_path)) as connection:
        connection.executescript(schema)


def create_lead(lead_data, database_path=DATABASE_PATH):
    """Insert one lead and return its new database id."""
    missing_fields = [
        field for field in ("name", "inquiry_date", "status")
        if not lead_data.get(field)
    ]
    if missing_fields:
        raise ValueError(f"Missing required lead fields: {', '.join(missing_fields)}")

    placeholders = ", ".join(f":{field}" for field in LEAD_FIELDS)
    columns = ", ".join(LEAD_FIELDS)
    values = {field: lead_data.get(field) for field in LEAD_FIELDS}

    with closing(get_database_connection(database_path)) as connection:
        with connection:
            cursor = connection.execute(
                f"INSERT INTO leads ({columns}) VALUES ({placeholders})",
                values,
            )
            return cursor.lastrowid


def get_lead(lead_id, database_path=DATABASE_PATH):
    """Return one lead as a dictionary, or None if it does not exist."""
    with closing(get_database_connection(database_path)) as connection:
        row = connection.execute(
            "SELECT * FROM leads WHERE id = ?",
            (lead_id,),
        ).fetchone()
        return dict(row) if row is not None else None


def _follow_up_date_parameters(today=None):
    if today is None:
        today = date.today().isoformat()
    due_soon_until = (date.fromisoformat(today) + timedelta(days=7)).isoformat()
    return {"today": today, "due_soon_until": due_soon_until}


def _follow_up_status_sql():
    return """CASE
        WHEN leads.next_follow_up_date IS NULL
             OR trim(leads.next_follow_up_date) = ''
            THEN 'NO FOLLOW-UP'
        WHEN date(leads.next_follow_up_date) < date(:today)
            THEN 'OVERDUE'
        WHEN date(leads.next_follow_up_date) = date(:today)
            THEN 'DUE TODAY'
        WHEN date(leads.next_follow_up_date) <= date(:due_soon_until)
            THEN 'DUE SOON'
        ELSE 'UPCOMING'
    END"""


def get_lead_profile(lead_id, today=None, database_path=DATABASE_PATH):
    """Return lead details plus calculated follow-up status and last contact."""
    parameters = _follow_up_date_parameters(today)
    parameters["lead_id"] = lead_id
    query = f"""
        SELECT
            leads.*,
            MAX(follow_ups.contact_date) AS last_contact_date,
            {_follow_up_status_sql()} AS follow_up_status
        FROM leads
        LEFT JOIN follow_ups ON follow_ups.lead_id = leads.id
        WHERE leads.id = :lead_id
        GROUP BY leads.id
    """

    with closing(get_database_connection(database_path)) as connection:
        row = connection.execute(query, parameters).fetchone()
        return dict(row) if row is not None else None


def get_all_leads(include_archived=False, database_path=DATABASE_PATH):
    """Return leads newest first, excluding archived leads by default."""
    query = "SELECT * FROM leads"
    if not include_archived:
        query += " WHERE archived_at IS NULL"
    query += " ORDER BY created_at DESC, id DESC"

    with closing(get_database_connection(database_path)) as connection:
        rows = connection.execute(query).fetchall()
        return [dict(row) for row in rows]


def get_leads_for_list(
    search="",
    status="",
    source="",
    follow_up="",
    include_inactive=False,
    today=None,
    database_path=DATABASE_PATH,
):
    """Find and prioritize leads for the searchable lead list."""
    parameters = _follow_up_date_parameters(today)
    parameters.update({
        "search_pattern": f"%{search}%",
        "status": status,
        "source": source,
        "follow_up": follow_up,
        "include_inactive": include_inactive,
    })
    parameters.update(_ACTIVE_STATUS_PARAMETERS)
    query = f"""
        WITH lead_rows AS (
            SELECT
                leads.*,
                MAX(follow_ups.contact_date) AS last_contact_date,
                {_follow_up_status_sql()} AS follow_up_status
            FROM leads
            LEFT JOIN follow_ups ON follow_ups.lead_id = leads.id
            WHERE (
                :include_inactive
                OR (
                    leads.archived_at IS NULL
                    AND leads.status IN ({_ACTIVE_STATUS_SQL})
                )
            )
            AND (:search_pattern = '%%'
                 OR leads.name LIKE :search_pattern COLLATE NOCASE
                 OR COALESCE(leads.phone, '') LIKE :search_pattern COLLATE NOCASE
                 OR COALESCE(leads.company, '') LIKE :search_pattern COLLATE NOCASE
                 OR COALESCE(leads.location, '') LIKE :search_pattern COLLATE NOCASE)
            AND (:status = '' OR leads.status = :status)
            AND (:source = '' OR leads.source = :source)
            GROUP BY leads.id
        )
        SELECT * FROM lead_rows
        WHERE (:follow_up = '' OR follow_up_status = :follow_up)
        ORDER BY
            CASE follow_up_status
                WHEN 'OVERDUE' THEN 0
                WHEN 'DUE TODAY' THEN 1
                WHEN 'DUE SOON' THEN 2
                WHEN 'NO FOLLOW-UP' THEN 3
                ELSE 4
            END,
            CASE WHEN follow_up_status IN (
                'OVERDUE', 'DUE TODAY', 'DUE SOON', 'UPCOMING'
            ) THEN date(next_follow_up_date) END ASC,
            CASE WHEN follow_up_status = 'NO FOLLOW-UP' THEN inquiry_date END ASC,
            inquiry_date ASC,
            id ASC
    """

    with closing(get_database_connection(database_path)) as connection:
        rows = connection.execute(query, parameters).fetchall()
        return [dict(row) for row in rows]


def get_sales_action_queue(today=None, database_path=DATABASE_PATH):
    """Return active, unarchived leads grouped in attention-priority order."""
    parameters = _follow_up_date_parameters(today)
    parameters.update(_ACTIVE_STATUS_PARAMETERS)
    query = f"""
        SELECT
            leads.*,
            MAX(follow_ups.contact_date) AS last_contact_date,
            {_follow_up_status_sql()} AS follow_up_status,
            (
                SELECT latest_follow_up.customer_response
                FROM follow_ups AS latest_follow_up
                WHERE latest_follow_up.lead_id = leads.id
                                    AND latest_follow_up.customer_response IS NOT NULL
                                    AND trim(latest_follow_up.customer_response) <> ''
                ORDER BY latest_follow_up.contact_date DESC, latest_follow_up.id DESC
                LIMIT 1
            ) AS latest_customer_response
        FROM leads
        LEFT JOIN follow_ups ON follow_ups.lead_id = leads.id
        WHERE leads.archived_at IS NULL
          AND leads.status IN ({_ACTIVE_STATUS_SQL})
        GROUP BY leads.id
        ORDER BY
            CASE follow_up_status
                WHEN 'OVERDUE' THEN 0
                WHEN 'DUE TODAY' THEN 1
                WHEN 'DUE SOON' THEN 2
                WHEN 'NO FOLLOW-UP' THEN 3
                ELSE 4
            END,
            CASE WHEN follow_up_status IN (
                'OVERDUE', 'DUE SOON', 'UPCOMING'
            ) THEN date(leads.next_follow_up_date) END ASC,
            CASE WHEN follow_up_status = 'DUE TODAY'
                THEN COALESCE(leads.next_action, '') END COLLATE NOCASE ASC,
            CASE WHEN follow_up_status = 'NO FOLLOW-UP'
                THEN leads.inquiry_date END ASC,
            leads.inquiry_date ASC,
            leads.id ASC
    """

    with closing(get_database_connection(database_path)) as connection:
        rows = connection.execute(query, parameters).fetchall()

    queue = {category: [] for category in SALES_QUEUE_CATEGORIES}
    for row in rows:
        lead = dict(row)
        queue[lead["follow_up_status"]].append(lead)
    return queue


def get_lead_count(database_path=DATABASE_PATH):
    """Return the number of leads, including archived leads."""
    with closing(get_database_connection(database_path)) as connection:
        row = connection.execute("SELECT COUNT(*) FROM leads").fetchone()
        return row[0]


def update_lead(lead_id, updates, database_path=DATABASE_PATH):
    """Update supplied lead fields and return whether a lead was found."""
    if not updates:
        raise ValueError("Provide at least one lead field to update.")

    unknown_fields = set(updates) - set(LEAD_FIELDS)
    if unknown_fields:
        raise ValueError(f"Fields cannot be updated: {', '.join(sorted(unknown_fields))}")

    assignments = ", ".join(f"{field} = :{field}" for field in updates)
    values = dict(updates)
    values["lead_id"] = lead_id

    with closing(get_database_connection(database_path)) as connection:
        with connection:
            cursor = connection.execute(
                f"UPDATE leads SET {assignments}, updated_at = :updated_at "
                "WHERE id = :lead_id",
                {**values, "updated_at": _timestamp_now()},
            )
            return cursor.rowcount > 0


def update_lead_status(lead_id, status, database_path=DATABASE_PATH):
    """Set a lead's sales status after validating the value against the allowed list."""
    if database_path is None:
        database_path = DATABASE_PATH
    if status not in LEAD_STATUSES:
        raise ValueError(f"Invalid sales status: {status}")

    with closing(get_database_connection(database_path)) as connection:
        with connection:
            cursor = connection.execute(
                "UPDATE leads SET status = ?, updated_at = ? WHERE id = ?",
                (status, _timestamp_now(), lead_id),
            )
            return cursor.rowcount > 0


def archive_lead(lead_id, database_path=DATABASE_PATH):
    """Mark a lead archived instead of permanently deleting it."""
    with closing(get_database_connection(database_path)) as connection:
        with connection:
            cursor = connection.execute(
                "UPDATE leads SET archived_at = COALESCE(archived_at, ?), "
                "updated_at = ? WHERE id = ?",
                (_timestamp_now(), _timestamp_now(), lead_id),
            )
            return cursor.rowcount > 0


def create_follow_up(follow_up_data, database_path=DATABASE_PATH):
    """Save an interaction and update the lead's current next action."""
    if not follow_up_data.get("contact_date"):
        raise ValueError("A follow-up contact_date is required.")

    follow_up_fields = (
        "lead_id",
        "contact_date",
        "contact_method",
        "what_happened",
        "customer_response",
        "outcome",
        "next_action",
        "next_follow_up_date",
    )
    values = {field: follow_up_data.get(field) for field in follow_up_fields}

    with closing(get_database_connection(database_path)) as connection:
        with connection:
            cursor = connection.execute(
                "INSERT INTO follow_ups ("
                "lead_id, contact_date, contact_method, what_happened, "
                "customer_response, outcome, next_action, next_follow_up_date"
                ") VALUES ("
                ":lead_id, :contact_date, :contact_method, :what_happened, "
                ":customer_response, :outcome, :next_action, :next_follow_up_date"
                ")",
                values,
            )
            connection.execute(
                "UPDATE leads SET next_action = :next_action, "
                "next_follow_up_date = :next_follow_up_date, "
                "updated_at = :updated_at WHERE id = :lead_id",
                {**values, "updated_at": _timestamp_now()},
            )
            return cursor.lastrowid


def get_follow_ups_for_lead(lead_id, database_path=DATABASE_PATH):
    """Return a lead's follow-up history, newest contact first."""
    with closing(get_database_connection(database_path)) as connection:
        rows = connection.execute(
            "SELECT * FROM follow_ups WHERE lead_id = ? "
            "ORDER BY contact_date DESC, id DESC",
            (lead_id,),
        ).fetchall()
        return [dict(row) for row in rows]