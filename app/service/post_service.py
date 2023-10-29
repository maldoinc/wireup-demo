from dataclasses import dataclass

from wireup import container

from app.model.api import PostCreateModel
from app.model.db import Post
from app.service import MailerService, PostRepository


@container.register
@dataclass
class PostService:
    repository: PostRepository
    mailer: MailerService

    def create_post(self, post: PostCreateModel) -> Post:
        new_post = Post(**post.model_dump())

        self.repository.save(new_post)
        self.mailer.notify_admin_for_post(new_post)

        return new_post
