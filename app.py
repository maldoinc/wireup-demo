import json
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
    container.params.put("mailer.email_dsn", os.environ.get("MAILER_DSN"))
    with open("./config/parameters.json") as f:
        container.params.update(json.loads(f.read()))

    return app


if __name__ == "__main__":
    create_app().run()
