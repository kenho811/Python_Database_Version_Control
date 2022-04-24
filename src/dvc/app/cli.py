"""
Define the main commands of the CLI
"""
import logging
from pathlib import Path

import psycopg2
import typer
from dvc.core.database.postgres import SQLFileExecutor
from dvc.core.config import generate_default_config_file, get_postgres_connection
from dvc.core.struct import SchemaRevision, Operation
from dvc.core import METADATA_SQL_FOLDER_PATH

# Set default logging to INFO
logging.root.setLevel(logging.INFO)

app = typer.Typer()

SQL_FILE_FOLDER_PATH: Path = Path("sample_revision_sql_files")




@app.command()
def init():
    generate_default_config_file()


@app.command()
def upgrade():
    """
    Upgrade the Current Database Version by applying a corresponding Upgrade Revision Version
    :return:
    """
    conn = get_postgres_connection()
    sql_file_path = SQL_FILE_FOLDER_PATH.joinpath("RV1__create_scm_fundamentals_and_tbls.upgrade.sql")
    revision = SchemaRevision(
        executed_sql_file_path_applied=sql_file_path,
        operation=Operation.Upgrade
    )
    sql_file_executor = SQLFileExecutor(conn=conn)
    sql_file_executor.execute_revision(schema_revision=revision)


@app.command()
def downgrade():
    """
    Downgrade the Current Database Version by applying a corresponding Downgrade Revision Version
    :return:
    """
    conn = get_postgres_connection()
    sql_file_path = SQL_FILE_FOLDER_PATH.joinpath("RV1__create_scm_fundamentals_and_tbls.downgrade.sql")
    revision = SchemaRevision(
        executed_sql_file_path_applied=sql_file_path,
        operation=Operation.Downgrade
    )
    sql_file_executor = SQLFileExecutor(conn=conn)
    sql_file_executor.execute_revision(schema_revision=revision)

@app.command()
def check():
    """
    Check the current Database Version
    :return:
    """
    conn = get_postgres_connection()
    sql_file_path = METADATA_SQL_FOLDER_PATH.joinpath("RV1__create_scm_fundamentals_and_tbls.downgrade.sql")
    revision = SchemaRevision(
        executed_sql_file_path_applied=sql_file_path,
        operation=Operation.Downgrade
    )
    sql_file_executor = SQLFileExecutor(conn=conn)
    sql_file_executor.execute_revision(schema_revision=revision)
