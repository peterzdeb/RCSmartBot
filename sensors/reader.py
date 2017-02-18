import asyncio
import aiofiles


class SensorsReader(object):
    
    def __init__(self):
        self.sensors = []
        self.reader_callback = lambda _: NotImplementedError

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    @asyncio.coroutine
    def process_sensors(self):
        print('sensors setup')
        for sensor in self.sensors:
            yield from sensor.setup()

        f = yield from aiofiles.open('actions.log', mode='w+')
        try:
            while True:
                for sensor in self.sensors:
                    data = yield from sensor.read()
                    yield from self.reader_callback('mocked_name', data)
        finally:
            yield from f.close()

    def register_handler(self, callback):
        self.reader_callback = callback