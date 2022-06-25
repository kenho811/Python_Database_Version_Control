import logging
import functools
import typer.models
from typing import Union
from pathlib import Path
import inspect

from dvc.core.config import ConfigReader, ConfigDefault


class SetRootLoggingLevel:
    """
    Used as a decorator to set the root logging level
    """
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self,
                 *args,
                 **kwargs):
        print(f"Get current logging level: {logging._levelToName[logging.getLogger().getEffectiveLevel()]}")
        config_file_path = kwargs.get('config_file_path')
        # print(config_file_path)

        if config_file_path is None:
            logging.warning("Cannot find logging_level. Using INFO")
            logging_level = logging.INFO
        else:
            config_reader = ConfigReader(config_file_path)
            logging_level = config_reader.logging_level
            logging.info(f"Logging Level found. Setting level to {logging._levelToName[logging_level]} ")

        logging.root.setLevel(logging_level)

        return self.func(*args, **kwargs)
