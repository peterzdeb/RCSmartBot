import aiofiles
import asyncio
import json

from .base_sensor import BaseSensorDevice


class SerialSensor(BaseSensorDevice):
    @asyncio.coroutine
    def setup(self):
        self._fd = yield from aiofiles.open(self.sensor_address)

    @asyncio.coroutine
    def read(self):
        data = yield from self._fd.readline()
        data = json.loads(data)

        measurements = []
        for sensor_type, records in data.items():
            measurements.append((sensor_type, list(records)))
            print("Received sensor data: %s", str(data))
        return measurements
