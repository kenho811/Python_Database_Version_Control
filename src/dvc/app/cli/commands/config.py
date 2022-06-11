"""
config subcommand
"""
import logging

import typer

from dvc.core.config import ConfigDefault, DatabaseRevisionFilesManager, ConfigFileWriter, ConfigReader

app = typer.Typer()


@app.command()
def init():
    """
    Generate configuration template
    """
    # Step 1: Generate config file
    config_file_writer = ConfigFileWriter(config_file_path=ConfigDefault.VAL__FILE_PATH)
    config_file_writer.write_to_yaml()

    # Step 2: Generate Datababase Revision SQL folder
    config_file_reader = ConfigReader(ConfigDefault.VAL__FILE_PATH)
    db_rv_files_man = DatabaseRevisionFilesManager(config_file_reader)
    db_rv_files_man.create_database_revision_files_folder()
