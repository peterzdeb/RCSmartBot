import aiofiles
import asyncio
import json
import logging

from smart_bot.sensors.base_sensor import BaseSensorDevice


trace_log = logging.getLogger('smart_bot.trace')
logger = logging.getLogger(__name__)

class SerialSensor(BaseSensorDevice):
    @asyncio.coroutine
    def setup(self):
        try:
            self._fd = yield from aiofiles.open(self.sensor_address, 'rb')
        except FileNotFoundError as e:
            logger.error('Failed to initialize Serial sensor(%s): %s', self.sensor_address, e)

    @asyncio.coroutine
    def read(self):
        if not self._fd:
            return []
        data = yield from self._fd.readline()
        trace_log.debug('Got data from serial sensor: %s', data)
        data = data.decode('utf8', 'replace')
        data = data.replace("'", '"').replace('}{', "}\n{")
        
        measurements = []
        for record in data.split('\n'):
            if not record.strip():
                continue
            trace_log.debug("Reading JSON from serial sensor: %s", record)
            try:
                data_dict = json.loads(record)
            except ValueError:
                trace_log.warning("Skipping malformed data: %s", record)
                continue
            for sensor_type, records in data_dict.items():
                measurements.append((sensor_type, list(records)))
        return measurements
