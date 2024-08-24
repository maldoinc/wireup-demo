import sys
from pathlib import Path

import click
from wireup import container

from demoapp.models.db import DbBaseModel
from demoapp.services.database_connection import DatabaseConnection


@click.command()
@container.autowire
def create_db(db: DatabaseConnection) -> None:
    path = Path(sys.argv[0]).parent.parent / "var"

    if not path.exists():
        Path.mkdir(path)

    DbBaseModel.metadata.create_all(db.engine)
