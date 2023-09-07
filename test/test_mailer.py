from unittest import TestCase

from model.app import EmailMessage, EmailAddress
from service import MailerService
from test.fixtures import _make_db_post


class TestMailer(TestCase):
    def setUp(self) -> None:
        self.mailer = MailerService(
            email_from_name="from_name",
            email_from_address="mailer@example.com",
            admin_name="Bob",
            admin_address="bob@example.com",
            email_dsn="smtp:///null",
        )

    def test_mailer_generates_email(self):
        email = self.mailer.make_email_from_post(_make_db_post(1))

        self.assertEqual(
            email,
            EmailMessage(
                from_address=EmailAddress(
                    name="from_name", address="mailer@example.com"
                ),
                to_addresses=[EmailAddress(name="Bob", address="bob@example.com")],
                subject="New blog post: title 1",
                body="A new blog entry was posted with the following contents: \n\ncontent 1",
            ),
        )
