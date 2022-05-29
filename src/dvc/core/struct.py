import datetime
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Operation(Enum):
    Upgrade = "upgrade"
    Downgrade = "downgrade"


@dataclass
class DatabaseRevision:
    executed_sql_file_path_applied: Path
    operation: Operation


@dataclass
class DatabaseVersion:
    current_version: str
    next_upgrade_revision_version: str
    next_downgrade_revision_version: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
