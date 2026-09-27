"""Temporary-database tests for the daily queue and existing lead workflows."""

import unittest
from datetime import date, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory

from app import app
from database import (
    archive_lead,
    create_follow_up,
    create_lead,
    get_all_leads,
    get_follow_ups_for_lead,
    get_lead_profile,
    get_sales_action_queue,
    initialize_database,
)


class SalesQueueTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = TemporaryDirectory(prefix="ngaoroofing-queue-test-")
        self.database_path = Path(self.temporary_directory.name) / "queue.sqlite3"
        self.original_database_path = app.config["DATABASE_PATH"]
        app.config["DATABASE_PATH"] = str(self.database_path)
        initialize_database(self.database_path)
        self.client = app.test_client()
        self.today = date.today()

    def tearDown(self):
        app.config["DATABASE_PATH"] = self.original_database_path
        self.temporary_directory.cleanup()

    def add_lead(
        self,
        name,
        status="NEW",
        follow_up_offset=None,
        inquiry_offset=30,
        next_action="Call customer",
        source="Referral",
        company="TEST DATA Roofing",
        location="Nairobi",
        phone="+254700123456",
    ):
        follow_up_date = None
        if follow_up_offset is not None:
            follow_up_date = (self.today + timedelta(days=follow_up_offset)).isoformat()
        return create_lead(
            {
                "name": f"TEST DATA - {name}",
                "company": company,
                "phone": phone,
                "location": location,
                "source": source,
                "project_type": "Commercial",
                "inquiry_date": (self.today - timedelta(days=inquiry_offset)).isoformat(),
                "status": status,
                "next_action": next_action,
                "next_follow_up_date": follow_up_date,
            },
            self.database_path,
        )

    def test_queue_categories_counts_order_and_closed_leads(self):
        oldest_overdue_id = self.add_lead("Oldest overdue", follow_up_offset=-10)
        self.add_lead("Recent overdue", status="QUOTED", follow_up_offset=-2)
        self.add_lead("Due today B", follow_up_offset=0, next_action="Zebra action")
        self.add_lead("Due today A", follow_up_offset=0, next_action="Ask about site")
        self.add_lead("Due soon", follow_up_offset=1)
        self.add_lead("Seven day boundary", follow_up_offset=7)
        self.add_lead("No date oldest", follow_up_offset=None, inquiry_offset=90)
        self.add_lead("No date newer", status="NEGOTIATION", follow_up_offset=None, inquiry_offset=10)
        self.add_lead("Upcoming soonest", follow_up_offset=8)
        self.add_lead("Upcoming later", follow_up_offset=20)

        create_follow_up(
            {
                "lead_id": oldest_overdue_id,
                "contact_date": (self.today - timedelta(days=1)).isoformat(),
                "contact_method": "Phone",
                "what_happened": "TEST DATA - Checked on the quotation.",
                "customer_response": "TEST DATA - Customer asked for a revised date.",
                "next_action": "Call customer again",
                "next_follow_up_date": (self.today - timedelta(days=10)).isoformat(),
            },
            self.database_path,
        )
        create_follow_up(
            {
                "lead_id": oldest_overdue_id,
                "contact_date": self.today.isoformat(),
                "contact_method": "Phone",
                "what_happened": "TEST DATA - Most recent interaction.",
                "next_action": "Call again",
                "next_follow_up_date": (self.today - timedelta(days=10)).isoformat(),
            },
            self.database_path,
        )

        for status in ("WON", "LOST", "DORMANT"):
            self.add_lead(f"Excluded {status}", status=status, follow_up_offset=0)
        archived_id = self.add_lead("Archived", follow_up_offset=-20)
        archive_lead(archived_id, self.database_path)

        queue = get_sales_action_queue(
            today=self.today.isoformat(),
            database_path=self.database_path,
        )
        self.assertEqual(
            list(queue),
            ["OVERDUE", "DUE TODAY", "DUE SOON", "NO FOLLOW-UP", "UPCOMING"],
        )
        self.assertEqual(len(queue["OVERDUE"]), 2)
        self.assertEqual(len(queue["DUE TODAY"]), 2)
        self.assertEqual(len(queue["DUE SOON"]), 2)
        self.assertEqual(len(queue["NO FOLLOW-UP"]), 2)
        self.assertEqual(len(queue["UPCOMING"]), 2)
        self.assertEqual(
            [lead["name"] for lead in queue["OVERDUE"]],
            ["TEST DATA - Oldest overdue", "TEST DATA - Recent overdue"],
        )
        self.assertEqual(
            [lead["name"] for lead in queue["DUE TODAY"]],
            ["TEST DATA - Due today A", "TEST DATA - Due today B"],
        )
        self.assertEqual(
            [lead["name"] for lead in queue["DUE SOON"]],
            ["TEST DATA - Due soon", "TEST DATA - Seven day boundary"],
        )
        self.assertEqual(queue["OVERDUE"][0]["last_contact_date"], self.today.isoformat())
        self.assertEqual(
            queue["OVERDUE"][0]["latest_customer_response"],
            "TEST DATA - Customer asked for a revised date.",
        )

        response = self.client.get("/")
        page = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        section_positions = [
            page.index(f'id="queue-{category.lower().replace(" ", "-")}"')
            for category in queue
        ]
        self.assertEqual(section_positions, sorted(section_positions))
        for category, count in (("OVERDUE", 2), ("DUE TODAY", 2), ("DUE SOON", 2), ("NO FOLLOW-UP", 2), ("UPCOMING", 2)):
            self.assertIn(f"{category} <span class=\"queue-count\">({count})</span>", page)
        for excluded_name in ("Excluded WON", "Excluded LOST", "Excluded DORMANT", "Archived"):
            self.assertNotIn(f"TEST DATA - {excluded_name}", page)
        self.assertIn(f'href="/leads/{oldest_overdue_id}"', page)
        self.assertIn("TEST DATA - Customer asked for a revised date.", page)
        self.assertIn("OPEN LEAD", page)

    def test_empty_queue_sections_and_main_navigation(self):
        response = self.client.get("/")
        page = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        for category, message in (
            ("OVERDUE", "No overdue follow-ups."),
            ("DUE TODAY", "No follow-ups due today."),
            ("DUE SOON", "No follow-ups due in the next 7 days."),
            ("NO FOLLOW-UP", "All active leads have a follow-up scheduled."),
            ("UPCOMING", "No upcoming follow-ups."),
        ):
            self.assertIn(f"{category} <span class=\"queue-count\">(0)</span>", page)
            self.assertIn(message, page)
        self.assertIn('href="/" aria-current="page">Sales Queue', page)
        self.assertIn('href="/leads">All Leads', page)
        self.assertIn('href="/leads/new">Add Lead', page)
        self.assertEqual(self.client.get("/leads").status_code, 200)
        self.assertEqual(self.client.get("/leads/new").status_code, 200)

    def test_add_lead_profile_and_follow_up_routes_still_work(self):
        form_page = self.client.get("/leads/new")
        self.assertIn(b'value="NEW" selected', form_page.data)

        invalid_lead = self.client.post(
            "/leads/new",
            data={"name": "", "inquiry_date": self.today.isoformat(), "status": "NEW"},
        )
        self.assertEqual(invalid_lead.status_code, 400)
        self.assertIn(b"Enter the lead&#39;s name.", invalid_lead.data)
        invalid_inquiry_date = self.client.post(
            "/leads/new",
            data={"name": "TEST DATA - Invalid date", "inquiry_date": "not-a-date", "status": "NEW"},
        )
        self.assertEqual(invalid_inquiry_date.status_code, 400)
        self.assertIn(b"Inquiry date must be a valid date.", invalid_inquiry_date.data)
        self.assertEqual(get_all_leads(database_path=self.database_path), [])

        lead_data = {
            "name": "TEST DATA - Workflow regression",
            "phone": "+254700987654",
            "email": "workflow@example.invalid",
            "company": "TEST DATA Company",
            "source": "Referral",
            "project_type": "Residential",
            "location": "Nairobi",
            "estimated_roof_area": "120",
            "product_profile": "Box profile",
            "inquiry_date": self.today.isoformat(),
            "status": "NEW",
            "notes": "TEST DATA only",
            "next_action": "Check quotation",
            "next_follow_up_date": (self.today + timedelta(days=10)).isoformat(),
        }
        saved = self.client.post("/leads/new", data=lead_data)
        self.assertEqual(saved.status_code, 302)
        lead_url = saved.location.split("?")[0]
        lead_id = int(lead_url.rsplit("/", 1)[1])
        empty_profile = self.client.get(lead_url)
        self.assertEqual(empty_profile.status_code, 200)
        self.assertIn(b"No follow-up interactions have been logged yet.", empty_profile.data)

        duplicate = self.client.post("/leads/new", data=lead_data)
        self.assertIn(b"Possible existing lead", duplicate.data)
        self.assertEqual(len(get_all_leads(database_path=self.database_path)), 1)
        filtered = self.client.get("/leads?q=workflow&status=NEW&source=Referral")
        self.assertIn(b"TEST DATA - Workflow regression", filtered.data)

        follow_up = self.client.post(
            f"{lead_url}/follow-ups",
            data={
                "contact_date": self.today.isoformat(),
                "contact_method": "Phone",
                "what_happened": "TEST DATA - Checked the quote.",
                "customer_response": "TEST DATA - Customer will review it.",
                "outcome": "Waiting for feedback.",
                "next_action": "Call in three days.",
                "next_follow_up_date": (self.today + timedelta(days=3)).isoformat(),
            },
        )
        self.assertEqual(follow_up.status_code, 302)
        self.assertIn(b"Follow-up logged.", self.client.get(follow_up.location).data)
        self.assertEqual(len(get_follow_ups_for_lead(lead_id, self.database_path)), 1)
        profile = get_lead_profile(lead_id, self.today.isoformat(), self.database_path)
        self.assertEqual(profile["next_action"], "Call in three days.")
        self.assertEqual(profile["follow_up_status"], "DUE SOON")
        self.assertEqual(self.client.get("/leads/99999").status_code, 404)
        self.assertEqual(
            self.client.post("/leads/99999/follow-ups", data={"contact_date": self.today.isoformat()}).status_code,
            404,
        )

    def test_all_leads_filters_and_profile_history_regressions(self):
        lead_id = self.add_lead(
            "Search target",
            status="QUOTED",
            follow_up_offset=-2,
            source="Referral",
            company="Cedar Roofing",
            location="Nairobi",
            phone="+254711111111",
        )
        self.add_lead(
            "Due today target",
            status="NEW",
            follow_up_offset=0,
            source="Phone",
            company="Lake Works",
            location="Mombasa",
            phone="+254722222222",
        )
        self.add_lead("Due soon target", status="FOLLOW-UP", follow_up_offset=3)
        self.add_lead("No-date target", status="NEGOTIATION", follow_up_offset=None)
        self.add_lead("Upcoming target", status="SITE VISIT", follow_up_offset=9)
        self.add_lead("WON target", status="WON", follow_up_offset=0)
        self.add_lead("LOST target", status="LOST", follow_up_offset=0)
        self.add_lead("DORMANT target", status="DORMANT", follow_up_offset=0)
        archived_id = self.add_lead("Archived target", status="NEW", follow_up_offset=-1)
        archive_lead(archived_id, self.database_path)

        create_follow_up(
            {
                "lead_id": lead_id,
                "contact_date": (self.today - timedelta(days=10)).isoformat(),
                "what_happened": "TEST DATA - older conversation",
                "customer_response": "TEST DATA - earlier response",
                "next_action": "Call customer",
                "next_follow_up_date": (self.today - timedelta(days=2)).isoformat(),
            },
            self.database_path,
        )
        create_follow_up(
            {
                "lead_id": lead_id,
                "contact_date": (self.today - timedelta(days=4)).isoformat(),
                "what_happened": "TEST DATA - latest conversation",
                "customer_response": "TEST DATA - latest response",
                "next_action": "Call customer",
                "next_follow_up_date": (self.today - timedelta(days=2)).isoformat(),
            },
            self.database_path,
        )

        for search in ("search target", "254711111111", "CEDAR", "nAiRoBi"):
            response = self.client.get("/leads", query_string={"q": search})
            self.assertIn(b"TEST DATA - Search target", response.data)
        self.assertIn(b"TEST DATA - Search target", self.client.get("/leads?status=QUOTED").data)
        self.assertIn(b"TEST DATA - Search target", self.client.get("/leads?source=Referral").data)
        self.assertIn(b"TEST DATA - Search target", self.client.get("/leads?follow_up=OVERDUE").data)
        self.assertIn(b"TEST DATA - Due today target", self.client.get("/leads?follow_up=DUE%20TODAY").data)
        self.assertIn(b"TEST DATA - Due soon target", self.client.get("/leads?follow_up=DUE%20SOON").data)
        self.assertIn(b"TEST DATA - No-date target", self.client.get("/leads?follow_up=NO%20FOLLOW-UP").data)
        self.assertIn(b"TEST DATA - Upcoming target", self.client.get("/leads?follow_up=UPCOMING").data)

        combined = self.client.get(
            "/leads",
            query_string={
                "q": "nAiRoBi",
                "status": "QUOTED",
                "source": "Referral",
                "follow_up": "OVERDUE",
            },
        )
        self.assertIn(f'href="/leads/{lead_id}"'.encode(), combined.data)
        active_page = self.client.get("/leads")
        for excluded_name in ("WON target", "LOST target", "DORMANT target", "Archived target"):
            self.assertNotIn(f"TEST DATA - {excluded_name}".encode(), active_page.data)
        all_page = self.client.get("/leads?scope=all")
        for included_name in ("WON target", "LOST target", "DORMANT target", "Archived target"):
            self.assertIn(f"TEST DATA - {included_name}".encode(), all_page.data)

        profile = self.client.get(f"/leads/{lead_id}")
        self.assertEqual(profile.status_code, 200)
        self.assertLess(
            profile.data.index(b"TEST DATA - latest conversation"),
            profile.data.index(b"TEST DATA - older conversation"),
        )
        self.assertIn(b"TEST DATA - latest response", profile.data)

        history_count = len(get_follow_ups_for_lead(lead_id, self.database_path))
        invalid_contact = self.client.post(
            f"/leads/{lead_id}/follow-ups",
            data={"contact_date": "not-a-date", "what_happened": "TEST DATA - preserved"},
        )
        self.assertEqual(invalid_contact.status_code, 400)
        self.assertIn(b"TEST DATA - preserved", invalid_contact.data)
        invalid_next_date = self.client.post(
            f"/leads/{lead_id}/follow-ups",
            data={
                "contact_date": self.today.isoformat(),
                "next_follow_up_date": "not-a-date",
                "what_happened": "TEST DATA - preserved",
            },
        )
        self.assertEqual(invalid_next_date.status_code, 400)
        self.assertEqual(len(get_follow_ups_for_lead(lead_id, self.database_path)), history_count)

    def test_status_change_profile_validation_queue_and_filter_regressions(self):
        lead_id = self.add_lead(
            "Status target",
            status="NEW",
            follow_up_offset=4,
            next_action="Validate the status form",
        )
        create_follow_up(
            {
                "lead_id": lead_id,
                "contact_date": (self.today - timedelta(days=3)).isoformat(),
                "contact_method": "Phone",
                "what_happened": "TEST DATA - Checked on the lead.",
                "customer_response": "TEST DATA - Customer asked for a revised quote.",
                "next_action": "Send revised quotation",
                "next_follow_up_date": (self.today + timedelta(days=2)).isoformat(),
            },
            self.database_path,
        )

        before_profile = get_lead_profile(lead_id, self.today.isoformat(), self.database_path)
        before_follow_ups = get_follow_ups_for_lead(lead_id, self.database_path)
        before_next_action = before_profile["next_action"]
        before_next_follow_up = before_profile["next_follow_up_date"]

        invalid_response = self.client.post(
            f"/leads/{lead_id}/status",
            data={"status": "INVALID STATUS"},
        )
        self.assertEqual(invalid_response.status_code, 302)
        invalid_page = self.client.get(invalid_response.location)
        self.assertEqual(invalid_page.status_code, 200)
        self.assertIn(b"Invalid sales status.", invalid_page.data)

        profile_after_invalid = get_lead_profile(lead_id, self.today.isoformat(), self.database_path)
        self.assertEqual(profile_after_invalid["status"], "NEW")
        self.assertEqual(profile_after_invalid["next_action"], before_next_action)
        self.assertEqual(profile_after_invalid["next_follow_up_date"], before_next_follow_up)
        self.assertEqual(len(get_follow_ups_for_lead(lead_id, self.database_path)), len(before_follow_ups))

        missing_response = self.client.post("/leads/99999/status", data={"status": "QUOTED"})
        self.assertEqual(missing_response.status_code, 404)

        success_response = self.client.post(
            f"/leads/{lead_id}/status",
            data={"status": "QUOTED"},
        )
        self.assertEqual(success_response.status_code, 302)
        success_page = self.client.get(success_response.location)
        self.assertEqual(success_page.status_code, 200)
        self.assertIn(b"Status updated.", success_page.data)

        quoted_profile = get_lead_profile(lead_id, self.today.isoformat(), self.database_path)
        self.assertEqual(quoted_profile["status"], "QUOTED")
        self.assertNotEqual(quoted_profile["updated_at"], before_profile["updated_at"])
        self.assertEqual(quoted_profile["next_action"], before_next_action)
        self.assertEqual(quoted_profile["next_follow_up_date"], before_next_follow_up)
        self.assertEqual(len(get_follow_ups_for_lead(lead_id, self.database_path)), len(before_follow_ups))
        self.assertIn(b"TEST DATA - Status target", self.client.get("/leads?status=QUOTED").data)

        self.client.post(f"/leads/{lead_id}/status", data={"status": "WON"})
        self.assertNotIn(
            "TEST DATA - Status target",
            [lead["name"] for lead in get_sales_action_queue(today=self.today.isoformat(), database_path=self.database_path)["OVERDUE"]],
        )
        self.assertIn(
            b"TEST DATA - Status target",
            self.client.get("/leads?status=WON&scope=all").data,
        )

        self.client.post(f"/leads/{lead_id}/status", data={"status": "NEW"})
        queue_after_reopen = get_sales_action_queue(today=self.today.isoformat(), database_path=self.database_path)
        lead_names = [lead["name"] for lead in queue_after_reopen["DUE SOON"] + queue_after_reopen["OVERDUE"] + queue_after_reopen["DUE TODAY"]]
        self.assertIn("TEST DATA - Status target", lead_names)
        self.assertIn(b"TEST DATA - Status target", self.client.get("/leads?status=NEW&scope=all").data)


if __name__ == "__main__":
    unittest.main()