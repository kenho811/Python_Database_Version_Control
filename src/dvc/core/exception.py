from enum import Enum
from pathlib import Path

from dvc.core.database import SupportedDatabaseFlavour
from dvc.core.struct import Operation


class RequestedDatabaseFlavourNotSupportedException(Exception):
    def __init__(self,
                 requested_database_flavour,
                 ):
        self.requested_database_flavour = requested_database_flavour

    def __str__(self):
        return f"""
        Your requested database flavour: {self.requested_database_flavour}
        Supported Database Flavours are:
        {[e.name for e in SupportedDatabaseFlavour]}
        """


class InvalidDatabaseRevisionFilesException(Exception):
    class Status(Enum):
        """
        List of all reasons
        """
        NON_CONFORMANT_REVISION_FILE_NAME_EXISTS = 101  # all files all follow 'RV{num}__{description}.{upgrade/downgrade}.sql' format
        MORE_REVISION_SQL_FILES_FOUND_THAN_REQUIRED_STEPS_SPECIFIED = 102  # Given specified number of steps, more targetrevision SQL Files are found
        FEWER_REVISION_SQL_FILES_FOUND_THAN_REQUIRED_STEPS_SPECIFIED = 103  # Given specified number of steps, fewer target revision SQL Files are found

    def __init__(self,
                 status: Status,
                 file_path: Path
                 ):
        self.status = status
        self.file_path = file_path

    def __str__(self):
        return f"""
        {self.status.name}
        {self.file_path}
        """


class DatabaseConnectionFailureException(Exception):

    def __init__(self,
                 ):
        pass

    def __str__(self):
        return "Something is wrong with the database connection!"

class OperationNotAccountedForException(Exception):
    """
    Operation not accounted for
    """

    def __init__(self,
                 operation_type = Operation
                 ):
        self.operation_type = operation_type

    def __str__(self):
        return f"Your Operation {self.operation_type} is NOT one of {[e.value for e in Operation]}"

class EnvironmentVariableNotSetException(Exception):

    def __init__(self,
                 missing_env_var: str
                 ):
        self.missing_env_var = missing_env_var

    def __str__(self):
        return f"""
        Did you set the environment variable {self.missing_env_var}???
        """
