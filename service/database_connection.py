from typing_extensions import Annotated

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from wireup import container, Wire


@container.register
class DatabaseConnection:
    def __init__(self, connection_url: Annotated[str, Wire(param="db.connection_str")]):
        self.engine = create_engine(connection_url)
        self._session = None

    @property
    def session(self) -> Session:
        if not self._session:
            self._session = sessionmaker(bind=self.engine)()

        return self._session
