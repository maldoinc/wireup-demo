from dataclasses import dataclass

from wireup import container

from app.model.api import PostGetModel
from app.model.db import Post
from app.service import DatabaseConnection


@container.register
@dataclass
class PostRepository:
    # Service injection is performed by the declared type so this
    # Does not need to use `Annotated`.
    db: DatabaseConnection

    def find_all(self) -> list[PostGetModel]:
        posts = self.db.session.query(Post).order_by(Post.created_at.desc()).all()

        return [PostGetModel.model_validate(p) for p in posts]

    def find_one_by_id(self, pk: int) -> PostGetModel | None:
        if post := self.db.session.get(Post, pk):
            return PostGetModel.model_validate(post)

        return None

    def save(self, post: Post) -> None:
        self.db.session.add(post)
        self.db.session.commit()
