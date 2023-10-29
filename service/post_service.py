from dataclasses import dataclass

from wireup import container

from model.api import PostCreateModel
from model.db import Post
from service import MailerService, PostRepository


@container.register
@dataclass
class PostService:
    repository: PostRepository
    mailer: MailerService

    def create_post(self, post: PostCreateModel) -> Post:
        new_post = self.repository.create(post)
        self.mailer.notify_admin_for_post(new_post)

        return new_post
