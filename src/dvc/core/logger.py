import logging
import functools
from typing import Union
from pathlib import Path

from dvc.core.config import ConfigReader, ConfigDefault


class SetRootLoggingLevel:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self,
                 config_file_path: Union[Path,str] = ConfigDefault.VAL__FILE_PATH,
                 *args,
                 **kwargs):
        config_reader = ConfigReader(config_file_path)
        logging_level = config_reader.logging_level
        logging.info(f"Setting level to {logging_level} ")
        logging.root.setLevel(logging_level)

        return self.func(*args, **kwargs)
