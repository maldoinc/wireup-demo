from dataclasses import dataclass

from wireup import service

from demoapp.models.api import PostView
from demoapp.models.db import Post
from demoapp.services.database_connection import DatabaseConnection


@service
@dataclass
class PostRepository:
    # Service injection is performed by the declared type so this
    # Does not need to use `Annotated`.
    db: DatabaseConnection

    def find_all(self) -> list[PostView]:
        posts = self.db.session.query(Post).order_by(Post.created_at.desc()).all()

        return [PostView.model_validate(p) for p in posts]

    def find_one_by_id(self, pk: int) -> PostView | None:
        if post := self.db.session.get(Post, pk):
            return PostView.model_validate(post)

        return None

    def save(self, post: Post) -> None:
        self.db.session.add(post)
        self.db.session.commit()
