import os

from flask import Flask
from pydantic import ValidationError
from wireup import container

import blueprint.post
import handler


def create_app() -> Flask:
    app = Flask(__name__)

    app.register_blueprint(blueprint.post.bp)
    app.register_error_handler(
        ValidationError, handler.jsonify_pydantic_validation_errors
    )

    container.params.put("db.connection_url", os.environ.get("DB_CONNECTION_URL"))

    return app


if __name__ == "__main__":
    create_app().run()
