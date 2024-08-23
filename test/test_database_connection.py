from unittest import TestCase

from demoapp.service.database_connection import DatabaseConnection


class DatabaseConnectionTest(TestCase):
    def test_db_reuses_same_session(self) -> None:
        db = DatabaseConnection("sqlite://")

        self.assertEqual(
            db.session,
            db.session,
            msg="Calling .session multiple times will reuse the same instance",
        )
