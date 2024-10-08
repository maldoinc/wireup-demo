import abc
from dataclasses import dataclass
from typing import Annotated

from wireup import Inject, abstract, service

from demoapp.models.api import PostView
from demoapp.models.app import EmailAddress, EmailMessage
from demoapp.models.config import NotificationMailerConfig


# Declare an abstract type as an "interface".
# This type cannot be directly instantiated by the container.
# It also doesn't HAVE to inherit from ABC either.
# This defines the contract for all services implementing MailerService
@abstract
class MailerService(abc.ABC):
    @abc.abstractmethod
    def notify_admin_for_post(self, post: PostView) -> None:
        raise NotImplementedError


# Register this as an implementation for MailerService.
# This class must directly inherit from the interface.
# When autowiring ask for the MailerService and this will get
# injected instead.
# See: https://maldoinc.github.io/wireup/latest/interfaces/
@service
@dataclass(frozen=True)
class MailerServiceImpl(MailerService):
    # Values in the parameter bag don't have to be scalar.
    # Structured data can also be used for configuration.
    # The alternative here would be to inject all the
    # fields of `notifier_config` as individual dependencies
    # which is not as nice.
    notifier_config: Annotated[
        NotificationMailerConfig,
        Inject(param="notification_mailer"),
    ]

    def notify_admin_for_post(self, post: PostView) -> None:
        self.send_email(self.make_email_from_post(post))

    def make_email_from_post(self, post: PostView) -> EmailMessage:
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
        print(
            f'Sending email: "{message.subject}",\n\n{message.body}.\n'
            f"from dsn {self.notifier_config.dsn}"
        )
