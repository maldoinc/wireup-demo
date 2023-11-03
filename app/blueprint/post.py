from typing import Annotated

from flask import Blueprint, Response, abort
from request_mapper import FromRequestBody
from wireup import Wire, container

from app.model.api import PostCreateModel
from app.service import PostRepository
from app.service.post_service import PostService
from app.util import ApiEndpoint, ApiResponse

bp = Blueprint("post", __name__, url_prefix="/posts")


@bp.get("/")
# Inject services by decorating methods with `@container.autowire`.
# Order can be important with decorators and this needs to be listed closer
# to the method than the flask one so that it is executed before it.
@container.autowire
def get_posts(post_repository: PostRepository) -> Response:
    return ApiResponse.ok(post_repository.find_all())


@bp.post("/")
@container.autowire
# Dependencies will get injected based on their type.
# Container will skip any unknown parameters so that
# wireup can be used in conjunction with other libraries or frameworks.
# In this case, "body" argument belongs to the request-mapper library.
def create_post(post_service: PostService, body: FromRequestBody[PostCreateModel]) -> Response:
    new_post = post_service.create_post(body)

    return ApiResponse.created(
        data=new_post,
        location=ApiEndpoint("post.get_post", post_id=new_post.id),
    )


@bp.get("/<int:post_id>")
@container.autowire
# Alternatively, if you want to be explicit about what will get injected
# you can annotate injected services with `Wire()`.
# If the container does not know about a type which is being explicitly asked
# to inject, it will raise an error.
def get_post(post_id: int, post_repository: Annotated[PostRepository, Wire()]) -> Response:
    if post := post_repository.find_one_by_id(post_id):
        return ApiResponse.ok(post)

    return abort(404)
