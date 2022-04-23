from pathlib import Path
from dataclasses import dataclass
from enum import Enum


@dataclass
class Operation(Enum):
    Upgrade = "upgrade"
    Downgrade = "downgrade"


@dataclass
class Revision:
    sql_file_path: Path
    operation: Operation
