import pytest
from typing import Dict
from pathlib import Path
import yaml
import logging

# Import fixtures
from tests.fixtures.database_revision import *
from tests.fixtures.postgres_service import *


@pytest.fixture()
def dummy_user_configuration_postgres_dict() -> Dict:
    """
    Fixture of User Configruration
    """
    DUMMY_USER_CONFIG_FILE: Dict = {
        "database_revision_sql_files_folder": "sample_revision_sql_files",
        "credentials": {
            "user": "peter_parker",
            "password": "1234",
            "host": "localhost",
            "port": 5432,
            "dbname": "superman_db",
            "dbflavour": "postgres"
        }
    }
    return DUMMY_USER_CONFIG_FILE


@pytest.fixture()
def dummy_config_file_path(tmp_path) -> Path:
    return tmp_path.joinpath('dummy_config_file_path.yaml')


@pytest.fixture
def init_dummy_config_file_path(
        dummy_config_file_path,
        dummy_user_configuration_postgres_dict):
    """
    Create a dummy config file with dummy configs
    """
    # Set up
    with open(dummy_config_file_path, 'w') as dummy_config_file:
        logging.info(f"creating file {dummy_config_file_path}")
        yaml.dump(dummy_user_configuration_postgres_dict, dummy_config_file, default_flow_style=False)
        yield

    # Tear down
    logging.info(f"deleting file {dummy_config_file_path}")
    dummy_config_file_path.unlink()

