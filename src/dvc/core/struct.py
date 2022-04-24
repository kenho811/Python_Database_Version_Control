import datetime
from pathlib import Path
from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class Operation(Enum):
    Upgrade = "upgrade"
    Downgrade = "downgrade"


@dataclass
class SchemaRevision:
    executed_sql_file_path_applied: Path
    operation: Operation
