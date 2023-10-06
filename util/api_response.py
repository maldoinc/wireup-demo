from typing import Optional

from flask import Response, jsonify, url_for
from pydantic import BaseModel
from sqlalchemy import inspect

from model.database import DbBaseModel

Model = BaseModel | DbBaseModel
ResponseObject = list[Model] | Model


def dump_model(model: Model):
    if isinstance(model, BaseModel):
        return model.model_dump()

    return {c.key: getattr(model, c.key) for c in inspect(model).mapper.column_attrs}


class ApiEndpoint:
    def __init__(self, name: str, **params):
        self.name = name
        self.params = params


class ApiResponse:
    @staticmethod
    def make(
        res: ResponseObject,
        status: int,
        headers: Optional[dict[str, str]] = None,
    ):
        response = ApiResponse._make_response(res)
        response.status_code = status
        if headers:
            response.headers.update(headers)

        return response

    @staticmethod
    def ok(data: ResponseObject):
        return ApiResponse.make(data, 200)

    @staticmethod
    def created(data: ResponseObject, location: ApiEndpoint):
        return ApiResponse.make(
            data,
            status=201,
            headers={
                "Location": url_for(
                    location.name, _external=True, **location.params
                )
            },
        )

    @staticmethod
    def _make_response(res: list[Model] | Model) -> Response:
        data = (
            [dump_model(x) for x in res] if isinstance(res, list) else dump_model(res)
        )

        return jsonify({"data": data})
