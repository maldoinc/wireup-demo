import yaml

from flask import Flask
from pydantic import ValidationError
from pyaml_env import parse_config
from wireup import container

import blueprint.post
import handler


def create_app() -> Flask:
    app = Flask(__name__)

    app.register_blueprint(blueprint.post.bp)
    app.register_error_handler(
        ValidationError, handler.jsonify_pydantic_validation_errors
    )

    all_config = parse_config("config/parameters.yaml", loader=yaml.UnsafeLoader)
    container.params.update(all_config["app"])

    return app


if __name__ == "__main__":
    create_app().run()
