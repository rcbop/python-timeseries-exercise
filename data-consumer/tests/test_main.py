from unittest.mock import Mock

import pytest
from consumer.main import main


@pytest.mark.unit
class TestMain:
    def test_main(self):
        consumer_worker_mock = Mock()
        main(consumer_worker_mock)
        consumer_worker_mock.run.assert_called_once()
