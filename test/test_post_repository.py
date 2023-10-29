import datetime
from test.fixtures import _make_api_post, _make_db_post
from unittest import TestCase

from model.api import PostCreateModel
from model.db import DbBaseModel
from service import DatabaseConnection, PostRepository


class DatabaseConnectionTest(TestCase):
    def setUp(self) -> None:
        self.db = DatabaseConnection("sqlite://")
        self.post_repository = PostRepository(self.db)

        DbBaseModel.metadata.create_all(self.db.engine)

    def tearDown(self) -> None:
        DbBaseModel.metadata.drop_all(self.db.engine)

    def test_fetches_all_posts_ordered_desc(self) -> None:
        self.db.session.add_all([_make_db_post(1), _make_db_post(2), _make_db_post(3)])
        self.db.session.commit()

        expected = [_make_api_post(3), _make_api_post(2), _make_api_post(1)]

        self.assertEqual(self.post_repository.find_all(), expected)

    def test_fetch_one_by_id_found_and_not_found(self) -> None:
        self.db.session.add_all([_make_db_post(1), _make_db_post(2)])

        self.assertEqual(self.post_repository.find_one_by_id(2), _make_api_post(2))
        self.assertEqual(self.post_repository.find_one_by_id(3), None)

    def test_create_post(self) -> None:
        request_model = PostCreateModel(
            title="My post",
            content="# Hello world",
            created_at=datetime.datetime(2023, 1, 1),
        )

        db_post = self.post_repository.create(request_model)
        self.db.session.commit()

        self.assertEqual(db_post.id, 1)
        self.assertEqual(db_post.title, request_model.title)
        self.assertEqual(db_post.content, request_model.content)
        self.assertEqual(db_post.created_at, request_model.created_at)
