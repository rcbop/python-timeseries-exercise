"""sensors generates data."""
from kink import inject
from sensor.bootstrap import bootstrap_di
from sensor.controller import SensorController


@inject
def main(sensor_controller: SensorController):
    sensor_controller.run()


if __name__ == "__main__":
    bootstrap_di()
    main()
