import unittest
from datetime import datetime
from test.fixtures import TestMailer

from app.model.api import PostCreateModel
from app.model.db import DbBaseModel
from app.service import DatabaseConnection, PostRepository
from app.service.post_service import PostService


class TestPostService(unittest.TestCase):
    def setUp(self) -> None:
        self.db = DatabaseConnection("sqlite://")
        self.mailer = TestMailer()
        DbBaseModel.metadata.create_all(self.db.engine)

    def test_creates_post_and_notifies(self) -> None:
        post_model = PostCreateModel(
            title="My post",
            content="# Hello world",
            created_at=datetime(2023, 1, 1),
        )
        repository = PostRepository(self.db)
        db_post = PostService(repository=repository, mailer=self.mailer).create_post(post_model)
        self.assertEqual(db_post.id, 1)
        self.assertEqual(self.mailer.mail_sent_for_post, db_post)
