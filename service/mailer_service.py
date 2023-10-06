from dataclasses import dataclass
from typing_extensions import Annotated

from wireup import container, Wire

from model.app import EmailMessage, EmailAddress
from model.config import NotificationMailerConfig
from model.database import Post


@container.register
@dataclass(frozen=True)
class MailerService:
    notifier_config: Annotated[
        NotificationMailerConfig, Wire(param="notification_mailer")
    ]

    def notify_admin_for_post(self, post: Post):
        self.send_email(self.make_email_from_post(post))

    def make_email_from_post(self, post: Post) -> EmailMessage:
        return EmailMessage(
            from_address=EmailAddress(
                name=self.notifier_config.from_name,
                address=self.notifier_config.from_address,
            ),
            to_addresses=[
                EmailAddress(
                    name=self.notifier_config.admin_name,
                    address=self.notifier_config.admin_address,
                )
            ],
            subject=f"New blog post: {post.title}",
            body=f"A new blog entry was posted with the following contents: \n\n{post.content}",
        )

    def send_email(self, message: EmailMessage):
        raise NotImplementedError(
            f"Cannot send message with subject {message.subject} from dsn {self.notifier_config.dsn}"
        )
