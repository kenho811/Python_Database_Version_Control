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

    def set_logging_level(self,
                          logging_level:int ):
        logging.info(f"Setting root logging level to {logging._levelToName[logging_level]} ")
        logging.root.setLevel(logging_level)


    def __call__(self,
                 *args,
                 **kwargs):
        """
        If no custom logging level is found, then use default logging level (INFO)

        :param args:
        :param kwargs:
        :return:
        """

        try:
            config_file_path = kwargs['config_file_path']
            config_reader = ConfigReader(config_file_path)
            logging_level = config_reader.logging_level
        except Exception as e:
            logging_level = ConfigDefault.VAL__LOGGING_LEVEL
            logging.warning(f"Cannot find logging_level. Using default {logging_level}")
            logging_level = logging._nameToLevel[logging_level]
        finally:
            self.set_logging_level(logging_level=logging_level)

        return self.func(*args, **kwargs)
