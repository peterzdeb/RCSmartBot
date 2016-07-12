#! /usr/bin/python

import asyncio
import numpy as np
import RPi.GPIO as GPIO
import time


class GPIODistance(object):
    def __init__(self, trig, echo):
        self.__trig = trig
        self.__echo = echo
        self.__start = None
        self.__history = []
        self.__last_val = 5

    @asyncio.coroutine
    def setup(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__trig, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.__echo, GPIO.IN)
        yield from asyncio.sleep(0.5)

    @asyncio.coroutine
    def get_distance(self):
        GPIO.output(self.__trig, GPIO.HIGH)
        asyncio.sleep(0.000015)
        GPIO.output(self.__trig, GPIO.LOW)
        start = time.time()
        while not GPIO.input(self.__echo):
            if time.time() - start > 0.1:
                return 5
        start = time.time()
        while GPIO.input(self.__echo):
            pass
        end = time.time()
        
        val = (end-start)*340/2
        self.__history.append(val)
        data = self.__history[len(self.__history)-3:-1]

        if val <  np.mean(data) - 2 * np.std(data):
            print('filtered outlier !!!!!!!!!!!!!!!!! --- %s' % val)
            return self.__last_val
        return val


