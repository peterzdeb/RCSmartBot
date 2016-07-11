#!/usr/bin/env python

import asyncio
import logging

from web_gamepad.gamepad_server import WebGamepadServer

from drive_car import car_motion_event
from read_distance import GPIODistance

ALL_SENSORS = [
    (37, 35),
    (33, 31),
    (11, 7),
]

@asyncio.coroutine
def process_sensors():
    sensor = GPIODistance(*ALL_SENSORS[0])
    print('sensors setup')
    yield from sensor.setup()
    print('distance loop')
    while True:
        distance = yield from sensor.get_distance()
        print("DIST: %.5f" % distance)
        yield from asyncio.sleep(1)


if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.DEBUG)
        log = logging.getLogger('WebGamepad')
        server = WebGamepadServer(host='0.0.0.0', port=8000, notify_callback=car_motion_event)
        loop = asyncio.get_event_loop()

        server.start()
        asyncio.ensure_future(process_sensors(), loop=loop)
        loop.run_forever()
#        main()
    finally:
        GPIO.cleanup()