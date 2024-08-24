import unittest
from datetime import datetime

from demoapp.models.api import PostCreateModel
from demoapp.models.db import DbBaseModel
from demoapp.services.database_connection import DatabaseConnection
from demoapp.services.post_repository import PostRepository
from demoapp.services.post_service import PostService
from tests.fixtures import TestMailer


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
        new_post = PostService(repository=repository, mailer=self.mailer).create_post(post_model)
        self.assertEqual(new_post.id, 1)
        self.assertEqual(self.mailer.mail_sent_for_post, new_post)
