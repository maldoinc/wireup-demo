from dataclasses import dataclass

from wireup import container, wire

from model.app import EmailMessage, EmailAddress
from model.database import Post


@container.register
@dataclass(frozen=True)
class MailerService:
    email_from_name: str = wire(param="mailer.from_name")
    email_from_address: str = wire(param="mailer.from_address")

    admin_name: str = wire(param="mailer.admin_name")
    admin_address: str = wire(param="mailer.admin_address")

    email_dsn: str = wire(param="mailer.email_dsn")

    def notify_admin_for_post(self, post: Post):
        self.send_email(self.make_email_from_post(post))

    def make_email_from_post(self, post: Post) -> EmailMessage:
        return EmailMessage(
            from_address=EmailAddress(
                name=self.email_from_name, address=self.email_from_address
            ),
            to_addresses=[
                EmailAddress(name=self.admin_name, address=self.admin_address)
            ],
            subject=f"New blog post: {post.title}",
            body=f"A new blog entry was posted with the following contents: \n\n{post.content}",
        )

    def send_email(self, message: EmailMessage):
        raise NotImplementedError(
            f"Cannot send message with subject {message.subject} from dsn {self.email_dsn}"
        )
