from datetime import datetime

from demoapp.models.api import PostView
from demoapp.models.db import Post
from demoapp.services.mailer_service import MailerService


def make_db_post(i: int) -> Post:
    return Post(
        title=f"title {i}",
        content=f"content {i}",
        created_at=datetime(2023, 1, i),
    )


def make_api_post(i: int) -> PostView:
    return PostView(
        id=i,
        title=f"title {i}",
        content=f"content {i}",
        created_at=datetime(2023, 1, i),
    )


class TestMailer(MailerService):
    def __init__(self) -> None:
        self.mail_sent_for_post = None

    def notify_admin_for_post(self, post: PostView) -> None:
        self.mail_sent_for_post = post
