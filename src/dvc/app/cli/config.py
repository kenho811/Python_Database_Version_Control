"""
config subcommand
"""

import typer

from dvc.core.config import write_default_config_file

app = typer.Typer()


@app.command()
def init():
    """
    Generate configuration template & Initialise database
    """
    # Step 1: Generate config file
    write_default_config_file()

