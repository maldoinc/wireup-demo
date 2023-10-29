from flask import Response, jsonify
from pydantic import ValidationError


def jsonify_pydantic_validation_errors(exc: ValidationError) -> tuple[Response, int]:
    return jsonify({"errors": exc.errors()}), 422