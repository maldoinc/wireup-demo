from datetime import datetime

from model.api import PostGetModel
from model.db import Post


def _make_db_post(i: int) -> Post:
    return Post(
        title=f"title {i}",
        content=f"content {i}",
        created_at=datetime(2023, 1, i),
    )


def _make_api_post(i: int) -> PostGetModel:
    return PostGetModel(
        id=i,
        title=f"title {i}",
        content=f"content {i}",
        created_at=datetime(2023, 1, i),
    )
