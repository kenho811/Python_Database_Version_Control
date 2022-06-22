from enum import Enum
from pathlib import Path
from typing import List, Optional

from dvc.core.database import SupportedDatabaseFlavour
from dvc.core.struct import Operation, DatabaseRevisionFile


class RequestedDatabaseFlavourNotSupportedException(Exception):
    """
    Exception raised when requested database flavour is not supported
    """

    def __init__(self,
                 requested_database_flavour: str,
                 ):
        self.requested_database_flavour = requested_database_flavour

    def __str__(self):
        return f"""
        Your requested database flavour: {self.requested_database_flavour}
        Supported Database Flavours are:
        {[e.name for e in SupportedDatabaseFlavour]}
        """


class InvalidDatabaseRevisionFilesException(Exception):
    """
    Exception Raised when something is wrong with the DatabaseRevisionFiles
    """

    class Status(Enum):
        """
        List of all reasons
        """
        NON_CONFORMANT_REVISION_FILE_NAME_EXISTS = 101  # all files all follow 'RV{num}__{description}.{upgrade/downgrade}.sql' format
        MORE_REVISION_SQL_FILES_FOUND_THAN_REQUIRED_STEPS_SPECIFIED = 102  # Given specified number of steps, more targetrevision SQL Files are found
        FEWER_REVISION_SQL_FILES_FOUND_THAN_REQUIRED_STEPS_SPECIFIED = 103  # Given specified number of steps, fewer target revision SQL Files are found
        NONCONSECUTIVE_REVISION_SQL_FILES_FOR_HEAD_OR_BASE_POINTER = 104 # Given head/base pointer, non-consecutive revision files are found

    def __init__(self,
                 status: Status,
                 config_file_path: Optional[Path],
                 database_revision_file_paths: List[Path],
                 ):
        self.status = status
        self.config_file_path = config_file_path
        self.database_revision_file_paths = database_revision_file_paths

    def __str__(self):
        return f"""
        Status: {self.status.name}
        Config file path: {self.config_file_path}
        Database Revision Files Paths Found: {self.database_revision_file_paths}
        """


class InvalidDatabaseVersionException(Exception):
    """
    Exception raised when format of Database Version is wrong
    """

    def __init__(self,
                 database_version: str,
                 ):
        self.database_version = database_version

    def __str__(self):
        return self.database_version


class DatabaseConnectionFailureException(Exception):
    """
    Exception raised when connection to the database fails
    """

    def __init__(self,
                 ):
        pass

    def __str__(self):
        return "Something is wrong with the database connection!"


class OperationNotAccountedForException(Exception):
    """
    Exception raised when operation is requested but is not yet developed
    """

    def __init__(self,
                 operation_type=Operation
                 ):
        self.operation_type = operation_type

    def __str__(self):
        return f"Your Operation {self.operation_type} is NOT one of {[e.value for e in Operation]}"


class EnvironmentVariableNotSetException(Exception):
    """
    Exception raised when required environment variables are not found
    """

    def __init__(self,
                 missing_env_var: str
                 ):
        self.missing_env_var = missing_env_var

    def __str__(self):
        return f"""
        Did you set the environment variable {self.missing_env_var}???
        """
