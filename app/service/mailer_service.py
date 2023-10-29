from dataclasses import dataclass
from typing import Annotated

from wireup import Wire, container

from app.model.app import EmailAddress, EmailMessage
from app.model.config import NotificationMailerConfig
from app.model.db import Post


@container.register
@dataclass(frozen=True)
class MailerService:
    notifier_config: Annotated[
        NotificationMailerConfig,
        Wire(param="notification_mailer"),
    ]

    def notify_admin_for_post(self, post: Post) -> None:
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
                ),
            ],
            subject=f"New blog post: {post.title}",
            body=f"A new blog entry was posted with the following contents: \n\n{post.content}",
        )

    def send_email(self, message: EmailMessage) -> None:
        msg = (
            f'Cannot send message with subject "{message.subject}" '
            f"from dsn {self.notifier_config.dsn}"
        )
        raise NotImplementedError(msg)
