import aiofiles
import asyncio

from .base_sensor import BaseSensorDevice


class SerialSensor(BaseSensorDevice):
    @asyncio.coroutine
    def setup(self):
        self.__fd = yield from aiofiles.open(self.sensor_address)
