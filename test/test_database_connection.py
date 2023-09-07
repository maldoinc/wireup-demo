from unittest import TestCase

from service import DatabaseConnection


class DatabaseConnectionTest(TestCase):
    def test_db_reuses_same_session(self):
        db = DatabaseConnection("sqlite://")

        self.assertEqual(
            db.session,
            db.session,
            msg="Calling .session multiple times will reuse the same instance",
        )
