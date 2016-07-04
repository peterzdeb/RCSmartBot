#!/usr/bin/env python

import RPi.GPIO as GPIO
import asyncio
import curses
import logging
import time

from gamepad_server import WebGamepadServer
 
GPIO.setmode(GPIO.BOARD)
  
Motor1A = 16
Motor1B = 18
Motor1E = 22
   
Motor2A = 19
Motor2B = 21
Motor2E = 23
    
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)
     
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)
      

def forward():
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
      
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)

def right():
    if is_back:
        left()
        return
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)
      
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)

def left():
    if is_back:
        right()
        return

    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
      
    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)
 
 

def backward():
    print("Going backwards")
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)
          
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)
 
 
def stop():
    if is_back or is_up or is_left or is_right:
        return
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)
 
is_up = False
is_back = False
is_left = False
is_right = False

def event(event):
    key = event.get('title')
    action = event.get('action')
    if key  == 'up':
        if action == 'key_down':
            is_up = True
            forward()
        elif action == 'key_up':
            is_up = False
            stop()
    if key  == 'down':
        if action == 'key_down':
            is_back = True
            backward()
        elif action == 'key_up':
            is_back = False
            stop()
    if key  == 'left':
        if action == 'key_down':
            is_left = True
            left()
        elif action == 'key_up':
            is_left = False
            stop()
    if key  == 'right':
        if action == 'key_down':
            is_right = True
            right()
        elif action == 'key_up':
            is_right = False
            stop()
           
    print(event)
    print(type(event))

def main(stdscr):
    # do not wait for input when calling getch
    stdscr.nodelay(1)
    #stdscr.timeout(-1)
    #curses.halfdelay(5)
    is_stopped = False
    last_pressed = time.time()
    while True:
        # get keyboard input, returns -1 if none available
        c = stdscr.getch()
        if c != -1:
            stdscr.addstr(str(c) + ' ')
            stdscr.refresh()
            last_pressed = time.time()
            if c == 258:
                if True:#is_stopped:
                    backward()
                else:
                    stop()
                    is_stopped = True
                    continue
            elif c == 259:
                forward()
            elif c == 261:
                right()
            elif c == 260:
                left()
            is_stopped = False
            last_pressed = time.time()
            # return curser to start position
        elif not is_stopped and time.time() - last_pressed > 0.06:
            stdscr.addstr('stopped')
            stdscr.refresh()
            stop()
            is_stopped = True
            #time.sleep(0.1)
        stdscr.move(0, 0)


static_path='static'

if __name__ == '__main__':
    try:
        server = WebGamepadServer
        logging.basicConfig(level=logging.DEBUG)
        log = logging.getLogger('WebGamepad')
        server = WebGamepadServer(host='0.0.0.0', port=8000, notify_callback=event)
        loop = asyncio.get_event_loop()
        server.start()
        loop.run_forever()
#        main()
    finally:
        GPIO.cleanup()
#        server.stop()

