from datetime import datetime, timezone

import click
from wireup import container

from demoapp.models.api import PostCreateModel
from demoapp.services.post_service import PostService


@click.command()
@click.argument("title")
@click.argument("contents")
@container.autowire
def create_post(title: str, contents: str, post_service: PostService) -> None:
    post = post_service.create_post(
        PostCreateModel(title=title, content=contents, created_at=datetime.now(tz=timezone.utc))
    )

    click.echo(f"Created post with id: {post.id}")
