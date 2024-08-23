import unittest
from datetime import datetime
from test.fixtures import TestMailer

from demoapp.model.api import PostCreateModel
from demoapp.model.db import DbBaseModel
from demoapp.service.database_connection import DatabaseConnection
from demoapp.service.post_repository import PostRepository
from demoapp.service.post_service import PostService


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
