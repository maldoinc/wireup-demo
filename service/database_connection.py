from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from typing_extensions import Annotated
from wireup import Wire, container


@container.register
class DatabaseConnection:
    def __init__(self, connection_url: Annotated[str, Wire(param="db_connection_url")]):
        self.engine = create_engine(connection_url)
        self._session = None

    @property
    def session(self) -> Session:
        if not self._session:
            self._session = sessionmaker(bind=self.engine)()

        return self._session
