"""Exercise the database using a temporary file, never the business database."""

from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from database import (
    create_follow_up,
    create_lead,
    get_database_connection,
    get_follow_ups_for_lead,
    get_lead,
    initialize_database,
)


def run_database_test():
    with TemporaryDirectory(prefix="ngaoroofing-test-") as temporary_directory:
        test_database_path = Path(temporary_directory) / "test_leads.sqlite3"
        initialize_database(test_database_path)

        lead_id = create_lead(
            {
                "name": "TEST DATA - Amina Njeri",
                "phone": "+254700123456",
                "email": "test.amina@example.invalid",
                "company": "TEST DATA - Amina Home",
                "source": "Referral",
                "project_type": "Residential",
                "location": "TEST DATA - Ruiru",
                "estimated_roof_area": 180.0,
                "product_profile": "Box profile roofing sheets",
                "inquiry_date": "2026-09-27",
                "status": "NEW",
                "notes": "TEST DATA only. Do not contact.",
                "next_action": "Confirm the preferred site visit date.",
                "next_follow_up_date": "2026-09-29",
            },
            test_database_path,
        )

        lead = get_lead(lead_id, test_database_path)
        assert lead is not None
        assert lead["name"] == "TEST DATA - Amina Njeri"

        follow_up_id = create_follow_up(
            {
                "lead_id": lead_id,
                "contact_date": "2026-09-27",
                "contact_method": "WhatsApp",
                "what_happened": "TEST DATA - Asked whether the site is ready for a visit.",
                "customer_response": "TEST DATA - Customer expects the slab ready on 2 October.",
                "outcome": "TEST DATA - Waiting for site readiness.",
                "next_action": "TEST DATA - Contact customer on 2 October.",
                "next_follow_up_date": "2026-10-02",
            },
            test_database_path,
        )

        follow_ups = get_follow_ups_for_lead(lead_id, test_database_path)
        assert len(follow_ups) == 1
        assert follow_ups[0]["id"] == follow_up_id
        assert follow_ups[0]["lead_id"] == lead_id

        with closing(get_database_connection(test_database_path)) as connection:
            foreign_keys_enabled = connection.execute(
                "PRAGMA foreign_keys"
            ).fetchone()[0]
        assert foreign_keys_enabled == 1

        # The next lookup uses a new connection after the prior one was closed.
        reopened_lead = get_lead(lead_id, test_database_path)
        reopened_history = get_follow_ups_for_lead(lead_id, test_database_path)
        assert reopened_lead["next_action"] == "TEST DATA - Contact customer on 2 October."
        assert reopened_lead["next_follow_up_date"] == "2026-10-02"
        assert len(reopened_history) == 1

    print("PASS: lead created and retrieved")
    print("PASS: follow-up linked to the correct lead")
    print("PASS: foreign-key enforcement is enabled")
    print("PASS: lead and follow-up persist after closing and reopening")
    print("PASS: test data was stored only in a temporary database")


if __name__ == "__main__":
    run_database_test()