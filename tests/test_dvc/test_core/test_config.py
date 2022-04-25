import yaml
from typing import Dict

from dvc.core.config import read_config_file


def test_read_config_file(monkeypatch):
    """
    GIVEN a monkeypatched version of yaml.load
    WHEN read_config_file is called
    THEN check read_config_file returns the python dict from yaml.load
    """
    def mock_load(*args, **kwargs) -> Dict:
        return {
            "key_1": "val_1",
            "key_2": "val_2"
        }

    monkeypatch.setattr(yaml, "load", mock_load)
    assert read_config_file() == {
        "key_1": "val_1",
        "key_2": "val_2"
    }
