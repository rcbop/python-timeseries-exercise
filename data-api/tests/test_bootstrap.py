from unittest.mock import Mock, patch

import pytest
from api.bootstrap import EnvConfig, bootstrap_di, get_env_config
from api.constants import (DEFAULT_MONGO_DB_NAME,
                           DEFAULT_MONGO_TS_COLLECTION_NAME, DEFAULT_MONGO_URI)


@pytest.fixture
def fix_env_config() -> EnvConfig:
    return EnvConfig(
        DEFAULT_MONGO_URI, DEFAULT_MONGO_DB_NAME, DEFAULT_MONGO_TS_COLLECTION_NAME)


@patch("api.bootstrap.MongoClient")
@patch("api.bootstrap.get_env_config")
@patch("api.bootstrap.logging.getLogger")
@patch("api.bootstrap.di")
def test_bootstrap_di(di_mock: Mock, logger_mock: Mock, get_env_config_mock: Mock, mongo_client_mock: Mock, fix_env_config: EnvConfig):
    get_env_config_mock.return_value = fix_env_config
    bootstrap_di()
    logger_mock.assert_called()
    get_env_config_mock.assert_called()
    mongo_client_mock.assert_called_once_with(DEFAULT_MONGO_URI)
    di_mock.__setitem__.assert_called()


def test_get_env_config_default_values(fix_env_config: EnvConfig):
    config = get_env_config()
    assert config == fix_env_config
