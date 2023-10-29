from dataclasses import dataclass
from typing import Annotated

from wireup import Wire, container

from app.model.app import EmailAddress, EmailMessage
from app.model.config import NotificationMailerConfig
from app.model.db import Post


# Register a mailer service. Registration can be done on dataclasses as well,
# although a services does not usually transfer data.
# The dataclass decorator provides an `__init__` method which the container makes use of.
# So this is really just a shorter way to define an init method.
#
# Despite how this might look this is still "constructor" injection
# rather than field injection which is deliberately NOT supported.
#
# Order here is important and @dataclass must be closer to the
# class declaration so that it is executed before `container.register`.
@container.register
@dataclass(frozen=True)
class MailerService:
    # Values in the parameter bag don't have to be scalar.
    # Structured data can also be used for configuration.
    # The alternative here would be to inject all the
    # fields of `notifier_config` as individual dependencies
    # which is not as nice.
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
