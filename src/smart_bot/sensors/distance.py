#! /usr/bin/python

import asyncio
import time

import numpy as np
import RPi.GPIO as GPIO

from smart_bot.sensors.base_sensor import BaseSensorDevice


class GPIODistance(BaseSensorDevice):

    def __init__(self, trig, echo):
        self.__trig = trig
        self.__echo = echo
        self.__start = None
        self.__history = []
        self.__last_val = 5
        super(GPIODistance, self).__init__()

    @asyncio.coroutine
    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__trig, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.__echo, GPIO.IN)
        yield from asyncio.sleep(2)

    @asyncio.coroutine
    def read(self):
        yield from asyncio.sleep(0.04)
        GPIO.output(self.__trig, GPIO.HIGH)
        time.sleep(0.00015)
        GPIO.output(self.__trig, GPIO.LOW)
        start = time.time()
        while GPIO.input(self.__echo) == 0:
            if time.time() - start > 0.003:
                return self.__last_val
        start = time.time()
        while GPIO.input(self.__echo) == 1:
            pass
        end = time.time()
        
        val = round((end-start)*340/2, 4)
        self.__history.append(val)
        del self.__history[:-10]#len(self.__history)-10:-1]

        if np.mean(self.__history) + 2.5 * np.std(self.__history) < val or val <  np.mean(self.__history) - 2.5 * np.std(self.__history):
            print('filtered outlier !!!!!!!!!!!!!!!!! --- %s' % val)
            return self.__last_val
        self.__last_val = val
        return float(val)
