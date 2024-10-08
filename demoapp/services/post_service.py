from dataclasses import dataclass

from wireup import service

from demoapp.models.api import PostCreateModel, PostView
from demoapp.models.db import Post
from demoapp.services.mailer_service import MailerService
from demoapp.services.post_repository import PostRepository


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
@service
@dataclass
class PostService:
    repository: PostRepository
    mailer: MailerService

    def create_post(self, post: PostCreateModel) -> PostView:
        new_post = Post(**post.model_dump())

        self.repository.save(new_post)

        post_view = PostView(
            id=new_post.id,
            title=new_post.title,
            content=new_post.content,
            created_at=new_post.created_at,
        )
        self.mailer.notify_admin_for_post(post_view)

        return post_view
