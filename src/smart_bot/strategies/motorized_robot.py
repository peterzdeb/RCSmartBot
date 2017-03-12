import asyncio

from smart_bot.motor_engine.motor_driver import MotorDriver, DualMotorDriver
from smart_bot.motor_engine.servo_driver import ServoDriver
from smart_bot.strategies.base_strategy import BaseRobotStrategy


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
    def on_stop(self, active=True):
        if not self.motor.stopped:
            self.__log_data['action'] = 'down_end'
            self.motor.stop()


class MotorizedSteeringRobotStrategy(BaseRobotStrategy):

    def __init__(self, log=None):
        super(MotorizedSteeringRobotStrategy, self).__init__()
        self.loop = asyncio.get_event_loop()
        self.initial_step = 20
        self.steering_tick = 0.1

        self.turning_left = False
        self.turning_right = False

        self.motor = MotorDriver(16, 18, 22)
        self.steer = ServoDriver(0)

    @asyncio.coroutine
    def on_forward(self, active=True, progress=None):
        if active:
            self.log_data['action'] = 'down_start'
            self.motor.forward()
        else:
            yield from self.on_stop()

    @asyncio.coroutine
    def on_backward(self, active=True, progress=None):
        if active:
            self.motor.backward()
        else:
            yield from self.on_stop()

    @asyncio.coroutine
    def on_left(self, active=True, progress=None):
        if active:
            self.turning_left = True
            self.turning_right = False
            self.loop.create_task(self.steer_left(progress))
        else:
            self.turning_left = False

    @asyncio.coroutine
    def on_right(self, active=True, progress=None):
        if active:
            self.turning_right = True
            self.turning_left = False
            self.loop.create_task(self.steer_right(progress))
        else:
            self.turning_right = False

    @asyncio.coroutine
    def on_stop(self, active=True):
        if not self.motor.stopped:
            self.log_data['action'] = 'down_end'
            self.motor.stop()

    @asyncio.coroutine
    def steer_left(self, progress=None):
        steps_pct = progress or self.initial_step

        while self.turning_left:
            self.steer.turn_left(steps_pct)
            if steps_pct == 100:
                break
            #step += step
            yield from asyncio.sleep(self.steering_tick)

    @asyncio.coroutine
    def steer_right(self, progress=None):
        steps_pct = progress or self.initial_step
        while self.turning_right:
            self.steer.turn_right(steps_pct)
            if steps_pct == 100:
                break
            #step += step
            yield from asyncio.sleep(self.steering_tick)
