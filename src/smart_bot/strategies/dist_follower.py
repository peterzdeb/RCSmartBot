import asyncio
import logging

from smart_bot.strategies.base_strategy import BaseRobotStrategy
from smart_bot.strategies.motorized_robot import MotorizedSteeringRobotStrategy


logger = logging.getLogger(__name__)


class StickyDistFollower(BaseRobotStrategy):

    def __init__(self, log=None):
        super(StickyDistFollower, self).__init__()
        self.__locked = False
        self.__moving = False
        self.__log = log
        self.distances = {}

    def sensor_handler(self, name, data):
        yield from self.recalculate_distances(data)

    @asyncio.coroutine
    def recalculate_distances(self, distances):
        distances = distances[:3]
        logger.debug('Recalc distances: %s', distances)
        self.log_data = {'dists': distances}

        min_dist = min(distances)
        max_dist = max(distances)
        print(min_dist)
        if min_dist < 10:
            logger.info('Criticaly close to obstacle. Emergency stopping...')
            yield from self.on_stop()
        elif min_dist < 20:
            logger.info('Trying to overcome obstacle...')
            yield from self.__start_relocating(distances)
        elif min_dist < 100:
            logger.info('Found a target to follow in %scm. Chasing...', 100)
            yield from self.__start_following(distances)
        else:
            logger.info('Nothing to follow. Stopping...')
        #        print("finish proc dists")
        yield from self.log()

    @asyncio.coroutine
    def __start_relocating(self, dists):
        yield from self.on_stop()
        
        print("<><><><><><><><><><><><><><><>")
        if dists[0] < dists[2] and dists[2] >= 10:
            yield from self.on_left(progress=100)
        elif dists[0] >= dists[2] and dists[0] >= 10:
            yield from self.on_right(progress=100)
        yield from self.on_backward()

    @asyncio.coroutine
    def __start_following(self, dists):
        print("Following: %s" % dists)
        if dists[2] <= dists[0] and dists[1] - dists[2] > 5:
            yield from self.on_right()
        elif dists[2] > dists[0] and dists[1] - dists[0] > 5:
            yield from self.on_left()
        yield from self.on_forward()

    @asyncio.coroutine
    def __turn_right(self):
        if self.__locked:
            return
        self.log_data['action'] = 'right_start'
        yield from self.log()
        self.__locked = True
        yield from asyncio.sleep(0.15)
        self.log_data['action'] = 'right_end'
        self.__locked = False


class MotorizedSteeringDistFollower(MotorizedSteeringRobotStrategy, StickyDistFollower):
    pass