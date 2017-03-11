import aiofiles
import asyncio
import json

from .base_sensor import BaseSensorDevice


class SerialSensor(BaseSensorDevice):
    @asyncio.coroutine
    def setup(self):
        self._fd = yield from aiofiles.open(self.sensor_address, 'rb')

    @asyncio.coroutine
    def read(self):
        data = yield from self._fd.readline()
        print(data)
        data = data.decode('utf8', 'replace')
        data = data.replace("'", '"').replace('}{', "}\n{")
        
        measurements = []
        for record in data.split('\n'):
            if not record.strip():
                continue
            print("Reading JSON from serial sensor: %s" % record)
            try:
                data_dict = json.loads(record)
            except ValueError:
                print("Skipping malformed data: %s", record)
                continue
            for sensor_type, records in data_dict.items():
                measurements.append((sensor_type, list(records)))
        return measurements
