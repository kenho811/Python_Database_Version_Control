from __future__ import annotations

import datetime
import logging
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List
import re


class Operation(Enum):
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
        self.file_path = file_path
        self._validate_sql_file_name()

    @classmethod
    def get_dummy_revision_file(
            cls,
            revision_number: int,
            operation_type: Operation,
    ) -> DatabaseRevisionFile:
        """
        Return
        :param revision_number:
        :param operation_type:
        :return:
        """
        dummy_file_path = Path(f"RV{revision_number}__dummy_file.{operation_type.value}.sql")
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
                file_path=self.file_path,
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
        Get the revision number
        """
        ending = self.file_path.name.split('.')[-1]
        return ending

    @property
    def description(self) -> str:
        """
        Get the revision number
        """
        description = self.file_path.name.split('__')[1]
        return description

    @property
    def revision_number(self) -> int:
        """
        Get the revision number
        """
        revision_number = int(self.file_path.name.split('__')[0][2:])
        return revision_number

    @property
    def operation_type(self) -> Operation:
        """
        Get the operation type
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
                 current_version: str,
                 created_at: Optional[datetime.datetime] = None
                 ):
        self._current_version = current_version
        self._created_at = created_at

        self._validate_database_version()

    def _validate_database_version(self):
        """
        Check if the name of a given file is a valid DatabaseRevisionFile
        :param instance:
        :return:
        """
        from dvc.core.exception import InvalidDatabaseVersionExceptio

        prog = re.compile(self.__class__.STANDARD_DATABASE_VERSION_FORMAT_REGEX)
        match = prog.match(self._current_version)
        if not match:
            raise InvalidDatabaseVersionExceptio(
                database_version=self._current_version)

    @property
    def current_version(self):
        return self._current_version

    @property
    def next_upgrade_database_revision_file(self) -> DatabaseRevisionFile:
        file = DatabaseRevisionFile.get_dummy_revision_file(
            revision_number=self.current_version_number + 1,
            operation_type=Operation.Upgrade,
        )
        return file

    @property
    def next_downgrade_database_revision_file(self) -> DatabaseRevisionFile:
        if self.current_version_number == 0:
            # No downgrade for version is V0
            return NotImplemented
        else:
            file = DatabaseRevisionFile.get_dummy_revision_file(
                revision_number=self.current_version_number,
                operation_type=Operation.Downgrade,
            )
        return file

    @property
    def created_at(self):
        if self._created_at is None:
            """
            Not yet persisted
            """
            logging.error(f"The Database Version {self._current_version} is a dummy database version!")
            return NotImplemented
        else:
            return self._created_at

    @property
    def current_version_number(self) -> int:
        return int(self.current_version[1:])

    def __add__(self, other) -> DatabaseVersion:
        """
        Apply DatabaseRevisionFile to DatabaseVersion
        :param other:
        :return:
        """
        if not isinstance(other, DatabaseRevisionFile):
            return NotImplemented

        current_version_number = self.current_version_number

        if other == self.next_upgrade_database_revision_file:
            return DatabaseVersion(current_version=f"V{self.current_version_number + 1}",
                                   created_at=None)
        elif other == self.next_downgrade_database_revision_file:
            return DatabaseVersion(current_version=f"V{self.current_version_number - 1}",
                                   created_at=None)
        else:
            raise ValueError(
                f"The revision file {other} CANNOT be applied to the database version {self._current_version}")

    def __sub__(self, other) -> List[DatabaseRevisionFile]:
        if not isinstance(other, DatabaseVersion):
            return NotImplemented

        database_revision_files: List[DatabaseRevisionFile] = []

        if self.current_version_number > other.current_version_number:
            # return a list of upgrade files
            for i in range(self.current_version_number, self.current_version_number - other.current_version_number):
                database_revision_files.append(
                    DatabaseRevisionFile.get_dummy_revision_file(revision_number=i,
                                                                 operation_type=Operation.Upgrade,
                                                                 )
                )
        elif self.current_version_number < other.current_version_number:
            # return a list of downgrade files
            for i in range(other.current_version_number, other.current_version_number - self.current_version_number):
                database_revision_files.append(
                    DatabaseRevisionFile.get_dummy_revision_file(revision_number=i,
                                                                 operation_type=Operation.Downgrade,
                                                                 )
                )
        else:
            # Do nothing
            pass

        return database_revision_files
