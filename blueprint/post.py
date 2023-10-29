from flask import Blueprint, Response, abort, request
from wireup import container

from model.api import PostCreateModel
from service import PostRepository
from service.post_service import PostService
from util import ApiEndpoint, ApiResponse

bp = Blueprint("post", __name__, url_prefix="/posts")


@bp.get("/")
@container.autowire
def get_posts(post_repository: PostRepository) -> Response:
    return ApiResponse.ok(post_repository.find_all())


@bp.post("/")
@container.autowire
def create_post(post_service: PostService) -> Response:
    new_post = post_service.create_post(PostCreateModel.model_validate(request.json))

    return ApiResponse.created(
        data=new_post,
        location=ApiEndpoint("post.get_post", post_id=new_post.id),
    )


@bp.get("/<int:post_id>")
@container.autowire
def get_post(post_id: int, post_repository: PostRepository) -> Response:
    if post := post_repository.find_one_by_id(post_id):
        return ApiResponse.ok(post)

    return abort(404)
