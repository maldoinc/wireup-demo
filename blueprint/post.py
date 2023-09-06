from flask import Blueprint, abort, request
from wireup import container

from model.api import PostCreateModel
from service import DatabaseConnection, PostRepository
from util import ApiResponse, ApiEndpoint

bp = Blueprint("post", __name__, url_prefix="/posts")


@bp.get("/")
@container.autowire
def get_posts(post_repository: PostRepository):
    return ApiResponse.ok(post_repository.find_all())


@bp.post("/")
@container.autowire
def create_post(db: DatabaseConnection, post_repository: PostRepository):
    new_post = post_repository.create(PostCreateModel.model_validate(request.json))
    db.session.commit()

    return ApiResponse.created(
        data=new_post, endpoint=ApiEndpoint("post.get_post", post_id=new_post.id)
    )


@bp.get("/<int:post_id>")
@container.autowire
def get_post(post_id, post_repository: PostRepository):
    if post := post_repository.find_one_by_id(post_id):
        return ApiResponse.ok(post)

    return abort(404)
