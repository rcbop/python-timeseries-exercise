from unittest.mock import Mock

import pytest
from sensor.main import main


@pytest.mark.unit
class TestMain:
    def test_main(self):
        mocked_sensor_controller = Mock()
        mocked_sensor_controller.run = Mock()
        main(mocked_sensor_controller)
        mocked_sensor_controller.run.assert_called_once()
