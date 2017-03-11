import asyncio

from motor_engine.motor_driver import MotorDriver, DualMotorDriver
from .base_strategy import BaseRobotStrategy
from .motorized_robot import MotorizedSteeringRobotStrategy

class StickyDistFollower(MotorizedSteeringRobotStrategy):

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
        self.log_data = {'dists': distances}
        min_dist = min(distances)
        max_dist = max(distances)
        print(min_dist)
        if min_dist > 1.5 or max_dist < 0.1:
            yield from self.on_stop()
        elif min_dist < 0.2:
            yield from self.__start_relocating(distances)
        elif min_dist < 1.5:
            yield from self.__start_following(distances)
        #        print("finish proc dists")
        yield from self.log()

    @asyncio.coroutine
    def __start_relocating(self, dists):
        yield from self.on_stop()
        
        print("<><><><><><><><><><><><><><><>")
        if dists[0] < dists[2] and dists[2] >= 0.1:
            yield from self.on_left()
        elif dists[0] >= dists[2] and dists[0] >= 0.1:
            yield from self.on_right()
        yield from self.on_backward()

    @asyncio.coroutine
    def __start_following(self, dists):
        print("Following: %s" % dists)
        if dists[2] <= dists[0] and dists[1] - dists[2] > 0.05:
            yield from self.on_right()
        elif dists[2] > dists[0] and dists[1] - dists[0] > 0.05:
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
