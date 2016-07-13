#!/usr/bin/env python

import asyncio
import logging
import numpy as np
import RPi.GPIO as GPIO

from follow_strategy import StickyDistFollower
from web_gamepad.gamepad_server import WebGamepadServer

from drive_car import car_motion_event
from read_distance import GPIODistance

ALL_SENSORS = [
    (37, 35),
    (33, 31),
    (11, 7),
]

def reject_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]

@asyncio.coroutine
def process_sensors():
    sensors = []
    for ports in ALL_SENSORS:
        sensors.append(GPIODistance(*ports))

    print('sensors setup')
    for sensor in sensors:
        yield from sensor.setup()
    print('distance loop')
    strategy = StickyDistFollower(car_motion_event)
    while True:
        dists = []
        for sensor in sensors:
            dist = yield from sensor.get_distance()
            dists.append(float(dist))
            yield from asyncio.sleep(0.06)
        print(dists)
        yield from strategy.process_distances(dists)



if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.DEBUG)
        log = logging.getLogger('WebGamepad')
        server = WebGamepadServer(host='0.0.0.0', port=8000, notify_callback=car_motion_event)
        loop = asyncio.get_event_loop()

        server.start()
        asyncio.async(process_sensors(), loop=loop)
        loop.run_forever()
#        main()
    finally:
        GPIO.cleanup()
