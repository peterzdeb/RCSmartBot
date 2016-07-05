#!/usr/bin/env python

import RPi.GPIO as GPIO
import asyncio
import curses
import logging
import time

from web_gamepad.gamepad_server import WebGamepadServer
 
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
      


active_keys = {}

def forward():
    print('going_forward')
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
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

def rotate_right():
    print('rotate_right')
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)

    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)

def turn_right(redirected=False):
    if 'up' not in active_keys and 'down' not in active_keys:
        rotate_right()
        return
    print('turn_right')
    GPIO.output(Motor2E,GPIO.LOW)
 

def rotate_left():
    print('rotate_left')
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)

    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)

def turn_left(redirected=False):
    if 'up' not in active_keys and 'down' not in active_keys:
        rotate_left()
        return
    print('turn left')
    GPIO.output(Motor1E,GPIO.LOW)

 
def stop():
    print('stopped')
    GPIO.output(Motor1E,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)

def refresh_engines():
    if 'up' in active_keys:
        forward()
    elif 'down' in active_keys:
        backward()
    if 'left' in active_keys:
        turn_left()
    elif 'right' in active_keys:
        turn_right()
    if not active_keys:
        stop()


def event(event):
    key = event.get('title')
    action = event.get('action')

    if action == 'key_down':
        active_keys[key] = 1
    elif action == 'key_up':
        del active_keys[key]
    print('keys: %s' % active_keys.keys())

    refresh_engines()

    print(event)

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

