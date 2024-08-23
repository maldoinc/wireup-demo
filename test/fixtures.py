from datetime import datetime

from demoapp.model.api import PostGetModel
from demoapp.model.db import Post
from demoapp.service.mailer_service import MailerService


def make_db_post(i: int) -> Post:
    return Post(
        title=f"title {i}",
        content=f"content {i}",
        created_at=datetime(2023, 1, i),
    )


def make_api_post(i: int) -> PostGetModel:
    return PostGetModel(
        id=i,
        title=f"title {i}",
        content=f"content {i}",
        created_at=datetime(2023, 1, i),
    )


class TestMailer(MailerService):
    def __init__(self) -> None:
        self.mail_sent_for_post = None

    def notify_admin_for_post(self, post: Post) -> None:
        self.mail_sent_for_post = post
