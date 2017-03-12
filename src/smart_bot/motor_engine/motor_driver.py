#!/usr/bin/env python

import asyncio
import logging

import smart_bot.utils

import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)

GPIO.setmode(GPIO.BOARD)

MOTOR_STOPPED = 0
MOTOR_FORWARD = 1
MOTOR_BACKWARD = 2


class MotorDriver(object):

    def __init__(self, input_a=16, input_b=18, enable=22):
        self._input_a = input_a
        self._input_b = input_b
        self._enable = enable
        self.run_mode = MOTOR_STOPPED
        self.reset()
        logger.info('Motor %(_enable)s: (in_a: %(_input_a)s, in_b: %(_input_b)s) is initialized',
                    self.__dict__)

    def reset(self):
        GPIO.setup(self._input_a,GPIO.OUT)
        GPIO.setup(self._input_b,GPIO.OUT)
        GPIO.setup(self._enable,GPIO.OUT)
        self.run_mode = MOTOR_STOPPED

    def forward(self):
        GPIO.output(self._input_a,GPIO.HIGH)
        GPIO.output(self._input_b,GPIO.LOW)
        GPIO.output(self._enable,GPIO.HIGH)
        self.run_mode = MOTOR_FORWARD
        logger.debug('Motor %d: Moving forward', self._enable)

    def backward(self):
        GPIO.output(self._input_a,GPIO.LOW)
        GPIO.output(self._input_b,GPIO.HIGH)
        GPIO.output(self._enable,GPIO.HIGH)
        self.run_mode = MOTOR_BACKWARD
        logger.debug('Motor %d: Moving backward', self._enable)

    def stop(self):
        GPIO.output(self._enable,GPIO.LOW)
        self.run_mode = MOTOR_STOPPED
        logger.debug('Motor %d: Stopped', self._enable)

    @property
    def moving_forward(self):
        return self.run_mode == MOTOR_FORWARD


    @property
    def moving_backward(self):
        return self.run_mode == MOTOR_BACKWARD

    @property
    def stopped(self):
        return self.run_mode == MOTOR_STOPPED


active_keys = {}

class DualMotorDriver(object):

    def __init__(self, motor_a, motor_b):
        self.motor_a = motor_a
        self.motor_b = motor_b
        self.in_reverse = False
        self.run_mode = MOTOR_STOPPED

    @property
    def is_forward(self):
        return self.run_mode == MOTOR_FORWARD

    @property
    def is_backward(self):
        return self.run_mode == MOTOR_BACKWARD

    def forward(self):
        logger.info('DualMotor: Moving Forward')
        self.motor_a.forward()
        self.motor_b.forward()
        self.run_mode = MOTOR_FORWARD

    def backward(self):
        logger.info('DualMotor: Moving Backwards')
        self.motor_a.backward()
        self.motor_b.backward()
        self.run_mode = MOTOR_BACKWARD

    def rotate_right(self):
        logger.info('DualMotor: Rotating Right')
        self.motor_a.forward()
        self.motor_b.backward()
        self.run_mode = MOTOR_STOPPED

    def turn_right(self, redirected=False):
        if self.motor_a.stopped and self.motor_b.stopped:
            self.rotate_right()
            return
        logger.info('DualMotor: Turning Right')
        self.motor_b.stop()

    def rotate_left(self):
        logger.info('DualMotor: Rotating Left')
        self.motor_a.backward()
        self.motor_b.forward()
        self.run_mode = MOTOR_STOPPED

    def turn_left(self):
        if self.motor_a.stopped and self.motor_b.stopped:
            self.rotate_left()
            return
        logger.info('DualMotor: Turning Left')
        self.motor_a.stop()

    def stop(self):
        logger.info('DualMotor: Full Stop')
        self.motor_a.stop()
        self.motor_b.stop()

    @property
    def stopped(self):
        return self.motor_a.stopped and self.motor_b.stopped
