from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Union

from dvc.core.struct import DatabaseRevisionFile, DatabaseVersion

from psycopg2._psycopg import connection


class SupportedDatabaseFlavour(Enum):
    """
    List of database flavours supported in the programme
    """
    Postgres = 'postgres'


DBConnLike = Union[
    # Postgres connection
    connection
]


class SQLFileExecutorTemplate(ABC):
    """
    Abstract Base Class for all SQLFileExecutors for different datbaases
    """

    def __init__(self,
                 db_conn: DBConnLike,
                 target_schema: str,
                 ):
        self.conn = db_conn
        self.target_schema = target_schema

    @abstractmethod
    def set_up_database_revision_control_tables(self):
        pass

    @abstractmethod
    def get_latest_database_version(self):
        pass

    @abstractmethod
    def execute_database_revision(self,
                                  database_revision: DatabaseRevisionFile
                                  ):
        pass
