import asyncio
import logging


trace_log = logging.getLogger('smart_bot.trace')


class SensorsReader(object):
    
    def __init__(self):
        self.sensors = []
        self.reader_callback = lambda _: NotImplementedError

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    @asyncio.coroutine
    def process_sensors(self):
        trace_log.info('Setting up %d sensors', len(self.sensors))
        for sensor in self.sensors:
            yield from sensor.setup()

        try:
            while True:
                for sensor in self.sensors:
                    trace_log.debug('Reading data from sensor: %s', sensor)
                    measurements = yield from sensor.read()
                    for sensor_type, data in measurements:
                        trace_log.debug("Sensor callback %s (%s)" % (sensor_type, data))
                        yield from self.reader_callback(sensor_type, data)
        finally:
            yield from self.stop()

    def register_handler(self, callback):
        self.reader_callback = callback
        
    @asyncio.coroutine
    def stop(self):
        for sensor in self.sensors:
            sensor.close()