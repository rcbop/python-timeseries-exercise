from unittest.mock import MagicMock, patch

import pytest
from consumer.model import MQTTConfig
from consumer.worker import KEEP_ALIVE, Worker


@pytest.mark.unit
class TestWorker:
    def test_worker_run(self):
        with patch("consumer.worker.mqtt.Client") as mqtt_client:
            logger = MagicMock()
            config = MQTTConfig(
                host="localhost",
                port=1883,
                topic="test",
            )
            sensor_dao = MagicMock()
            worker = Worker(logger, config, sensor_dao)
            worker.run()
            mqtt_client.assert_called_once()
            mqtt_client().connect.assert_called_once_with(
                config.host, config.port, KEEP_ALIVE)
            mqtt_client().subscribe.assert_called_once_with("#")
            mqtt_client().loop_forever.assert_called_once()
