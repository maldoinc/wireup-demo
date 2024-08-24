from typing import Annotated

import flask
from flask import Blueprint, Response, abort, jsonify
from wireup import Inject, container

from demoapp.models.api import PostCreateModel
from demoapp.services.post_repository import PostRepository
from demoapp.services.post_service import PostService
from demoapp.util import ApiEndpoint, ApiResponse

bp = Blueprint("post", __name__, url_prefix="/posts")


@bp.get("/")
# Inject services by decorating methods with `@container.autowire`.
# Order can be important with decorators and this needs to be listed closer
# to the method than the flask one so that it is executed before it.
@container.autowire
def get_posts(post_repository: PostRepository) -> Response:
    return jsonify(post_repository.find_all())


@bp.post("/")
@container.autowire
# Dependencies will get injected based on their type.
def create_post(post_service: PostService) -> Response:
    new_post = post_service.create_post(PostCreateModel(**flask.request.json))

    return ApiResponse.created(
        data=new_post,
        location=ApiEndpoint("post.get_post", post_id=new_post.id),
    )


@bp.get("/<int:post_id>")
@container.autowire
# Alternatively, if you want to be explicit about what will get injected
# you can annotate injected services with `Inject()`.
# If the container does not know about a type which is being explicitly asked
# to inject, it will raise an error.
def get_post(post_id: int, post_repository: Annotated[PostRepository, Inject()]) -> Response:
    if post := post_repository.find_one_by_id(post_id):
        return ApiResponse.ok(post)

    return abort(404)
