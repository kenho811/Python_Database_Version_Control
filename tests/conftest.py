import pytest
from typing import Dict

@pytest.fixture
def user_configuration_dict() -> Dict:
    """
    Fixture of User Configruration
    """
    USER_CONFIG_FILE: Dict = {
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
    return USER_CONFIG_FILE
