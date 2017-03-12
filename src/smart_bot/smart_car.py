import asyncio
import logging

from RPi import GPIO

from web_gamepad.gamepad_server import WebGamepadServer

from smart_bot.log_config import setup_loggers
from smart_bot.sensors.serial_sensor import SerialSensor
from smart_bot.sensors.reader import SensorsReader
from smart_bot import strategies
from smart_bot.strategies.dist_follower import MotorizedSteeringDistFollower


if __name__ == '__main__':
    setup_loggers()
    strategy = strategies.select_strategy(MotorizedSteeringDistFollower)

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
