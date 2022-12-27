"""test bootstrap module."""
import pytest
from unittest.mock import Mock, call, patch

from generator.bootstrap import (DEFAULT_COLLECTION_NAME, DEFAULT_DB_NAME,
                                 DEFAULT_MONGO_URI, bootstrap_db_config)

@pytest.mark.unit
class TestBootstrapModule:
    @patch("generator.bootstrap.os.getenv")
    def test_bootstrap_db_config(self, getenv_mock: Mock):
        bootstrap_db_config()

        getenv_mock.assert_has_calls([
            call("MONGO_URI", DEFAULT_MONGO_URI),
            call("MONGO_DB_NAME", DEFAULT_DB_NAME),
            call("MONGO_COLLECTION_NAME", DEFAULT_COLLECTION_NAME)])
