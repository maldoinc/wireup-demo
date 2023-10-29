from dataclasses import dataclass

from wireup import container

from model.api import PostGetModel
from model.db import Post
from service import DatabaseConnection


@container.register
@dataclass
class PostRepository:
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
