import yaml
from flask import Flask
from pyaml_env import parse_config
from pydantic import ValidationError
from wireup import container

from app import handler
from app.blueprint.post import bp as post_blueprint


def create_app() -> Flask:
    flask_app = Flask(__name__)

    flask_app.register_blueprint(post_blueprint)
    flask_app.register_error_handler(
        ValidationError,
        handler.jsonify_pydantic_validation_errors,
    )

    all_config = parse_config("config/parameters.yaml", loader=yaml.UnsafeLoader)
    container.params.update(all_config["app"])

    return flask_app


if __name__ == "__main__":
    create_app().run()
