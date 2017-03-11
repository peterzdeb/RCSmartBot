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

        try:
            while True:
                for sensor in self.sensors:
                    data = yield from sensor.read()
                    print("Sensor callback %s (%s)" % (type(sensor), data))
                    yield from self.reader_callback(type(sensor), data)
        finally:
            yield from self.stop()

    def register_handler(self, callback):
        self.reader_callback = callback
        
    @asyncio.coroutine
    def stop(self):
        for sensor in self.sensors:
            sensor.close()