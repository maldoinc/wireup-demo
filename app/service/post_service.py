from dataclasses import dataclass

from wireup import container

from app.model.api import PostCreateModel
from app.model.db import Post
from app.service import MailerService, PostRepository


# Register a Post service. Registration can be done on dataclasses as well,
# although a services does not usually transfer data.
# The dataclass decorator provides an `__init__` method which the container makes use of.
# So this is really just a shorter way to define an init method.
#
# Despite how this might look this is still "constructor" injection
# rather than field injection which is deliberately NOT supported.
#
# Order here is important and @dataclass must be closer to the
# class declaration so that it is executed before `container.register`.
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
