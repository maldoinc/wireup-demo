import yaml
from flask import Flask
from pyaml_env import parse_config
from request_mapper import setup_mapper
from request_mapper.integration.flask_integration import FlaskIntegration
from wireup import container

from app.blueprint.post import bp as post_blueprint


def create_app() -> Flask:
    flask_app = Flask(__name__)

    flask_app.register_blueprint(post_blueprint)
    setup_mapper(integration=FlaskIntegration(app=flask_app))

    # Load all configuration from yaml into a dictionary then register them in the container.
    # Services asking for parameter can reference them by name.
    # Note that types don't have to be just scalar values.
    # notification_mailer is a dataclass that will get injected as a parameter.
    all_config = parse_config("config/parameters.yaml", loader=yaml.UnsafeLoader)
    container.params.update(all_config["app"])

    return flask_app


if __name__ == "__main__":
    create_app().run()
