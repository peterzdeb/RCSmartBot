import asyncio

from motor_engine.motor_driver import MotorDriver, DualMotorDriver
from motor_engine.servo_driver import ServoDriver
from .base_strategy import BaseRobotStrategy


class DualMotorRobotStrategy(BaseRobotStrategy):

    def __init__(self, log=None):
        super(DualMotorRobotStrategy, self).__init__()
        self.__log_data = {}
        self.__locked = False
        self.__moving = False
        self.__log = log
        self.distances = {}

        motor_a = MotorDriver(16, 18, 22)
        motor_b = MotorDriver(19, 21, 23)
        self.motor = DualMotorDriver(motor_a, motor_b)

    @asyncio.coroutine
    def on_forward(self, active=True):
        if active:
            self.__log_data['action'] = 'down_start'
            self.motor.forward()
        else:
            yield from self.on_stop()

    @asyncio.coroutine
    def on_backward(self, active=True):
        if active:
            self.motor.backward()
        else:
            yield from self.on_stop()

    @asyncio.coroutine
    def on_left(self, active=True):
        if active:
            self.motor.turn_left()
        else:
            if self.motor.is_forward:
                yield from self.on_forward()
            elif self.motor.is_backward:
                yield from self.on_backward()
            else:
                yield from self.on_stop()

    @asyncio.coroutine
    def on_right(self, active=True):
        if active:
            self.motor.turn_right()
        else:
            if self.motor.is_forward:
                yield from self.on_forward()
            elif self.motor.is_backward:
                yield from self.on_backward()
            else:
                yield from self.on_stop()

    @asyncio.coroutine
    def on_stop(self):
        if not self.motor.stopped:
            self.__log_data['action'] = 'down_end'
            self.motor.stop()


class MotorizedSteeringRobotStrategy(BaseRobotStrategy):

    def __init__(self, log=None):
        super(MotorizedSteeringRobotStrategy, self).__init__()
        self.loop = asyncio.get_event_loop()
        self.initial_step = 20
        self.steering_tick = 0.5

        self.turning_left = False
        self.turning_right = False

        self.motor = MotorDriver(19, 21, 23)
        self.steer = ServoDriver(0)

    @asyncio.coroutine
    def on_forward(self, active=True):
        if active:
            self.log_data['action'] = 'down_start'
            self.motor.forward()
        else:
            yield from self.on_stop()

    @asyncio.coroutine
    def on_backward(self, active=True):
        if active:
            self.motor.backward()
        else:
            yield from self.on_stop()

    @asyncio.coroutine
    def on_left(self, active=True):
        if active:
            self.turning_left = True
            self.loop.create_task(self.steer_left())
        else:
            self.turning_left = False

    @asyncio.coroutine
    def on_right(self, active=True):
        if active:
            self.turning_right = True
            self.loop.create_task(self.steer_right())
        else:
            self.turning_right = False

    @asyncio.coroutine
    def on_stop(self):
        if not self.motor.stopped:
            self.log_data['action'] = 'down_end'
            self.motor.stop()

    @asyncio.coroutine
    def steer_left(self):
        step = self.initial_step
        while self.turning_left:
            self.steer.turn_left(step)
            step *= 2
            yield from asyncio.sleep(self.steering_tick)

    @asyncio.coroutine
    def steer_right(self):
        step = self.initial_step
        while self.turning_right:
            self.steer.turn_right(step)
            step *= 2
            yield from asyncio.sleep(self.steering_tick)
