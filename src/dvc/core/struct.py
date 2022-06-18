import datetime
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Operation(Enum):
    Upgrade = "upgrade"
    Downgrade = "downgrade"


class DatabaseRevisionFile:
    STANDARD_RV_FILE_FORMAT_REGEX = r'RV[0-9]*__.*\.(upgrade|downgrade)\.sql'

    def __init__(self,
                 file_path: Path
                 ):
        self.file_path = file_path

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


@dataclass
class DatabaseVersion:
    current_version: str
    next_upgrade_revision_version: str
    next_downgrade_revision_version: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
