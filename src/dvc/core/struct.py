from __future__ import annotations

import datetime
import logging
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
import re


class Operation(Enum):
    """
    Database Operations Allowed
    """
    Upgrade = "upgrade"
    Downgrade = "downgrade"


class DatabaseRevisionFile:
    """
    Raise error when File Path does not conform to standard
    """
    STANDARD_RV_FILE_FORMAT_REGEX = r'^RV[0-9]+__.*\.(upgrade|downgrade)\.sql$'

    def __init__(self,
                 file_path: Path
                 ):
        """
        :param file_path: Path pointing to the Database Revision File
        """
        self.file_path = file_path
        self._validate_sql_file_name()

    @classmethod
    def get_dummy_revision_file(
            cls,
            revision: str,
            operation_type: Operation,
    ) -> DatabaseRevisionFile:
        """
        Return a dummy revision file

        :param revision:
        :param operation_type:
        :return:
        """
        dummy_file_path = Path(f"{revision}__dummy_file.{operation_type.value}.sql")
        dummy_database_revision_file = cls(file_path=dummy_file_path)

        return dummy_database_revision_file

    def _validate_sql_file_name(self):
        """
        Check if the name of a given file is a valid DatabaseRevisionFile
        :param instance:
        :return:
        """
        from dvc.core.exception import InvalidDatabaseRevisionFilesException

        prog = re.compile(self.__class__.STANDARD_RV_FILE_FORMAT_REGEX)
        match = prog.match(self.file_path.name)
        if not match:
            raise InvalidDatabaseRevisionFilesException(
                config_file_path=self.file_path,
                status=InvalidDatabaseRevisionFilesException.Status.NON_CONFORMANT_REVISION_FILE_NAME_EXISTS)

    def __eq__(self, other) -> bool:
        """
        Determine when 2 SQL Revision files are the same
        :param other:
        :return:
        """

        if self.revision_number == other.revision_number and self.operation_type == other.operation_type:
            return True
        else:
            return False

    def __le__(self, other) -> bool:
        if self.revision_number < other.revision_number and self.operation_type == other.operation_type:
            return True
        else:
            return False

    def __gt__(self, other) -> bool:
        if self.revision_number > other.revision_number and self.operation_type == other.operation_type:
            return True
        else:
            return False

    @property
    def ending(self) -> str:
        """
        Get the file ending

        :return:
        """
        ending = self.file_path.name.split('.')[-1]
        return ending

    @property
    def description(self) -> str:
        """
        Get the file description

        :return:
        """
        description = self.file_path.name.split('__')[1]
        return description

    @property
    def revision_number(self) -> int:
        """
        Get the revision number

        :return:
        """
        revision_number = int(self.file_path.name.split('__')[0][2:])
        return revision_number

    @property
    def operation_type(self) -> Operation:
        """
        Get the operation type

        :return:
        """
        operation_type = self.file_path.name.split('.')[1]
        return Operation(operation_type)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"File Path: {self.file_path}"


class DatabaseVersion:
    STANDARD_DATABASE_VERSION_FORMAT_REGEX = r'^V[0-9]+$'

    def __init__(self,
                 version: str,
                 created_at: Optional[datetime.datetime] = None
                 ):
        self._version = version
        self._created_at = created_at

        self._validate_database_version()

    def _validate_database_version(self):
        """
        Check if the name of a given file is a valid DatabaseRevisionFile
        :param instance:
        :return:
        """
        from dvc.core.exception import InvalidDatabaseVersionException

        prog = re.compile(self.__class__.STANDARD_DATABASE_VERSION_FORMAT_REGEX)
        match = prog.match(self._version)
        if not match:
            raise InvalidDatabaseVersionException(
                database_version=self._version)

    @property
    def version(self):
        return self._version

    def __eq__(self, other):
        """
        Return boolean if two database versions are the same
        :param other:
        :return:
        """
        if not isinstance(other, DatabaseVersion):
            return NotImplemented

        if self.version == other.version and self.created_at == other.created_at:
            return True
        else:
            return False


    @property
    def next_upgrade_database_revision_file(self) -> DatabaseRevisionFile:
        """
        Get the database revision file for upgrade
        :return:
        """
        file = DatabaseRevisionFile.get_dummy_revision_file(
            revision=f"RV{self.version_number + 1}",
            operation_type=Operation.Upgrade,
        )
        return file

    @property
    def next_downgrade_database_revision_file(self) -> DatabaseRevisionFile:
        """
        Get the database revision file for downgrade
        :return:
        """
        if self.version_number == 0:
            # No downgrade for version is V0
            raise ValueError("Cannot downgrade with Version V0")
        else:
            file = DatabaseRevisionFile.get_dummy_revision_file(
                revision=f"RV{self.version_number}",
                operation_type=Operation.Downgrade,
            )
        return file

    @property
    def created_at(self):
        return self._created_at

    @property
    def version_number(self) -> int:
        return int(self.version[1:])

    def __add__(self, other) -> DatabaseVersion:
        """
        Get the theoretical new database version after applying a  DatabaseRevisionFile to given DatabaseVersion
        :param other:
        :return:
        """
        if not isinstance(other, DatabaseRevisionFile):
            return NotImplemented

        if other == self.next_upgrade_database_revision_file:
            return DatabaseVersion(version=f"V{self.version_number + 1}",
                                   created_at=None)
        elif other == self.next_downgrade_database_revision_file:
            return DatabaseVersion(version=f"V{self.version_number - 1}",
                                   created_at=None)
        else:
            raise ValueError(
                f"The revision file {other} CANNOT be applied to the database version {self._version}")

    def __sub__(self, other) -> List[DatabaseRevisionFile]:
        """
        Get a list of Database Revision Files required to change from the Current Database Version to the  Target Database Version

        Usage:
        self: target database version
        other: current database version

        :param other:
        :return:
        """
        if not isinstance(other, DatabaseVersion):
            return NotImplemented

        target_database_version = self
        current_database_version = other


        database_revision_files: List[DatabaseRevisionFile] = []

        if target_database_version.version_number > current_database_version.version_number:
            # return a list of upgrade files
            for i in range(current_database_version.version_number, target_database_version.version_number, 1):
                upgrade_revision_number = i + 1
                database_revision_files.append(
                    DatabaseRevisionFile.get_dummy_revision_file(revision=f"RV{upgrade_revision_number}",
                                                                 operation_type=Operation.Upgrade,
                                                                 )
                )
        elif target_database_version.version_number < current_database_version.version_number:
            # return a list of downgrade files
            for i in range(current_database_version.version_number, target_database_version.version_number, -1):
                downgrade_revision_number = i
                database_revision_files.append(
                    DatabaseRevisionFile.get_dummy_revision_file(revision=f"RV{downgrade_revision_number}",
                                                                 operation_type=Operation.Downgrade,
                                                                 )
                )
        elif self.version_number == other.version_number:
            # Do not append anything
            pass

        return database_revision_files

    def __str__(self):
        return f"""Database Version: {self._version}. Created at: {self.created_at}"""

    def __repr__(self):
        return self.__str__()

