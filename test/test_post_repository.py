import datetime
from test.fixtures import make_api_post, make_db_post
from unittest import TestCase

from app.model.db import DbBaseModel, Post
from app.service import DatabaseConnection, PostRepository


class DatabaseConnectionTest(TestCase):
    def setUp(self) -> None:
        self.db = DatabaseConnection("sqlite://")
        self.post_repository = PostRepository(self.db)

        DbBaseModel.metadata.create_all(self.db.engine)

    def tearDown(self) -> None:
        DbBaseModel.metadata.drop_all(self.db.engine)

    def test_fetches_all_posts_ordered_desc(self) -> None:
        self.db.session.add_all([make_db_post(1), make_db_post(2), make_db_post(3)])
        self.db.session.commit()

        expected = [make_api_post(3), make_api_post(2), make_api_post(1)]

        self.assertEqual(self.post_repository.find_all(), expected)

    def test_fetch_one_by_id_found_and_not_found(self) -> None:
        self.db.session.add_all([make_db_post(1), make_db_post(2)])

        self.assertEqual(self.post_repository.find_one_by_id(2), make_api_post(2))
        self.assertEqual(self.post_repository.find_one_by_id(3), None)

    def test_create_post(self) -> None:
        post = Post(
            title="My post",
            content="# Hello world",
            created_at=datetime.datetime(2023, 1, 1),
        )

        self.assertIsNone(post.id)
        self.post_repository.save(post)
        self.assertEqual(post.id, 1)
