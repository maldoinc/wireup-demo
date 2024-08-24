from pathlib import Path
from typing import Any

import yaml


def get_config() -> dict[str, Any]:
    # Load all configuration from yaml into a dict then register them in the container.
    # Services asking for parameter can reference them by name.
    # Note that types don't have to be just scalar values.
    # notification_mailer is a dataclass that will get injected as a parameter.
    app_dir = Path(__file__).parent.parent

    with Path.open(Path(f"{app_dir}/config/parameters.yaml")) as f:
        all_config = yaml.unsafe_load(f)

    return all_config["app"]
