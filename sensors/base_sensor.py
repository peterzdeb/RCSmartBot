import asyncio


class BaseSensorDevice(object):
    def __init__(self, sensor_address):
        self.sensor_address = sensor_address
        self._fd = None

    def __str__(self):
        return "%s (%s)" % (self.__class__.__name__, self.sensor_address)

    @asyncio.coroutine
    def setup(self):
        """self._fd must be defined here"""
        pass

    @asyncio.coroutine
    def read(self):
        data = yield from self._fd.readline()
        print("Received sensor data: %s", data)
        return data

    @asyncio.coroutine
    def close(self):
        if self._fd:
            yield from self._fd.close()
