from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from dvc.core.struct import DatabaseRevision, DatabaseVersion


class SQLFileExecutorTemplate(ABC):
    def __init__(self,
                 conn: Any
                 ):
        self.conn = conn

    @abstractmethod
    def set_up_database_revision_control_tables(self):
        pass

    @abstractmethod
    def get_latest_database_version(self):
        pass

    @abstractmethod
    def execute_database_revision(self,
                                  database_revision: DatabaseRevision
                                  ):
        pass


class SupportedDatabaseFlavour(Enum):
    """
    List of database flavours supported in the programme
    """
    Postgres = 'postgres'
