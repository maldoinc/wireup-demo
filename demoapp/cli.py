from wireup import container, initialize_container

from demoapp import services
from demoapp.commands import cli
from demoapp.config import get_config

if __name__ == "__main__":
    initialize_container(container, parameters=get_config(), service_modules=[services])
    cli()
