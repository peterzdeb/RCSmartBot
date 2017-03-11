import asyncio
import logging

from web_gamepad.gamepad_server import WebGamepadServer

from RPi import GPIO
from sensors.distance import GPIODistance
from sensors.serial_sensor import SerialSensor
from sensors.reader import SensorsReader
import strateries
from strateries.motorized_robot import MotorizedSteeringRobotStrategy


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(module)s.%(funcName)s %(message)s')

    strategy = strateries.select_strategy(MotorizedSteeringRobotStrategy)

    DISTANCE_SENSORS = [
        (37, 35),
        (33, 31),
        (11, 7),
    ]
    sensors_reader = SensorsReader()
    sensors_reader.add_sensor(SerialSensor('/dev/ttyUSB0'))
    #for port_trig, port_echo in DISTANCE_SENSORS:
    #    sensors_reader.add_sensor(GPIODistance(port_trig, port_echo))
    sensors_reader.register_handler(strategy.sensor_handler)

    try:
        loop = asyncio.get_event_loop()
        loop.create_task(sensors_reader.process_sensors())
        server = WebGamepadServer(host='0.0.0.0', port=8000, notify_callback=strategy.event_handler)
        server.start()
        loop.run_forever()
    finally:
        GPIO.cleanup()
