import asyncio
import logging

from Adafruit_PCA9685.PCA9685 import PCA9685


logger = logging.getLogger(__name__)


class MockPWM():
    def set_pwm(self, channel, on, off):
        logger.debug('Servo %d: changing position to %s', channel, off)

    def set_pwm_freq(self, *args, **kwargs):
        pass


class ServoDriver(object):

    def __init__(self, channel=0, min_position=300, max_position=470):
        self.__channel = channel
        self.step_position = min_position + (max_position - min_position) / 2
        self.min_position = min_position
        self.max_position = max_position
        self.total_steps = abs(self.max_position - self.min_position)
        try:
            self.pwm = PCA9685()
            self.pwm.set_pwm_freq(60)
        except Exception as e:
            logger.exception('Failed to initialize Servo Driver: %s', e)
            self.pwm = MockPWM()

    def turn_right(self, progress=10):
        step = progress / self.total_steps
        logger.info('Servo: turning right (%d%%) - step %d', progress, step)
        self.step_position = int(min(self.max_position, self.step_position + step))
        self.pwm.set_pwm(self.__channel, 0, self.step_position)

    def turn_left(self, progress=10):
        step = progress / self.total_steps
        logger.info('Servo: turning left (%d%%) - step %d', progress, step)
        self.step_position = int(max(self.min_position, self.step_position - step))
        self.pwm.set_pwm(self.__channel, 0, self.step_position)

    def set_servo_pulse(self, channel, pulse):
        pulse_length = 1000000    # 1,000,000 us per second
        pulse_length //= 60       # 60 Hz
        print('{0}us per period'.format(pulse_length))
        pulse_length //= 4096     # 12 bits of resolution
        print('{0}us per bit'.format(pulse_length))
        pulse *= 1000
        pulse //= pulse_length
        self.pwm.set_pwm(channel, 0, pulse)
