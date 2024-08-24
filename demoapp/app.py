from flask import Flask
from wireup.integration.flask_integration import wireup_init_flask_integration

from demoapp import services
from demoapp.blueprint.post import bp as post_blueprint
from demoapp.config import get_config


def create_app() -> Flask:
    flask_app = Flask(__name__)

    flask_app.register_blueprint(post_blueprint)
    flask_app.config.update(get_config())
    wireup_init_flask_integration(flask_app, service_modules=[services])

    return flask_app


if __name__ == "__main__":
    create_app().run()
