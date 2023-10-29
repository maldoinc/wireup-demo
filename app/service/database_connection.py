from typing import Annotated

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from wireup import Wire, container


@container.register
class DatabaseConnection:
    # DB service needs a connection DSN to work.
    # During application execution when this is managed and injected by the container,
    # `connection_url` will contain the value that was set in the parameter bag.
    #
    # During testing, you can manually provide a value.
    # The test suite uses `sqlite://` to have an in-memory sqlite connection
    # instead of storing it on disk.

    # Service init methods do not need to be decorated with @container.autowire.
    def __init__(self, connection_url: Annotated[str, Wire(param="db_connection_url")]) -> None:
        self.engine = create_engine(connection_url)
        self._session = None

    @property
    def session(self) -> Session:
        if not self._session:
            self._session = sessionmaker(bind=self.engine)()

        return self._session
