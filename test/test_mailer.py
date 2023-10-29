from test.fixtures import _make_db_post
from unittest import TestCase

from app.model.app import EmailAddress, EmailMessage
from app.model.config import NotificationMailerConfig
from app.service import MailerService


class TestMailer(TestCase):
    def setUp(self) -> None:
        self.mailer = MailerService(
            notifier_config=NotificationMailerConfig(
                from_name="from_name",
                from_address="mailer@example.com",
                admin_name="Bob",
                admin_address="bob@example.com",
                dsn="smtp:///null",
            ),
        )

    def test_mailer_generates_email(self) -> None:
        email = self.mailer.make_email_from_post(_make_db_post(1))

        self.assertEqual(
            email,
            EmailMessage(
                from_address=EmailAddress(
                    name="from_name",
                    address="mailer@example.com",
                ),
                to_addresses=[EmailAddress(name="Bob", address="bob@example.com")],
                subject="New blog post: title 1",
                body="A new blog entry was posted with the following contents: \n\ncontent 1",
            ),
        )
