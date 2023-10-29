import unittest
from datetime import datetime
from unittest.mock import MagicMock

from model.api import PostCreateModel
from model.db import DbBaseModel
from service import DatabaseConnection, PostRepository
from service.post_service import PostService


class TestPostService(unittest.TestCase):
    def setUp(self) -> None:
        self.db = DatabaseConnection("sqlite://")
        self.post_repository = PostRepository(self.db)

        DbBaseModel.metadata.create_all(self.db.engine)

    def test_creates_post_and_notifies(self) -> None:
        post_model = PostCreateModel(
            title="My post",
            content="# Hello world",
            created_at=datetime(2023, 1, 1),
        )
        repository = PostRepository(self.db)
        mailer = MagicMock()

        db_post = PostService(repository=repository, mailer=mailer).create_post(post_model)
        self.assertEqual(db_post.id, 1)
        mailer.notify_admin_for_post.assert_called_once_with(db_post)

