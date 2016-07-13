#! /usr/bin/python

import asyncio
import RPi.GPIO as GPIO
import time


class GPIODistance(object):
    def __init__(self, trig, echo):
        self.__trig = trig
        self.__echo = echo
        self.__start = None

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
        #while not GPIO.input(self.__echo):
        #    pass
        start = time.time()
        while GPIO.input(self.__echo):
            pass
        end = time.time()
        return (end-start)*340/2


