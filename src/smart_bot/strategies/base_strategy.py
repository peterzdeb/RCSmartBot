import asyncio
import logging


trace_log = logging.getLogger('smart_bot.trace')
logger = logging.getLogger(__name__)


class BaseRobotStrategy(object):

    def __init__(self):
        logger.info('Initializing %s strategy', self.__class__.__name__)
        self.active_actions = {}
        self.log_data = {}

    def on_stop(self, active=True):
        pass

    def on_forward(self, active=True, progress=None):
        pass

    def on_backward(self, active=True, progress=None):
        pass

    def on_left(self, active=True, progress=None):
        pass

    def on_right(self, active=True, progress=None):
        pass

    @asyncio.coroutine
    def sensor_handler(self, name, data):
        trace_log.debug('WARNING NotImplemented: Sensor "%s", data=%s' % (name, data))

    @asyncio.coroutine
    def event_handler(self, **event_data):
        """ Must be implemented for each strategy """
        #TODO: move into WebGamepad package
        trace_log.debug('Processing event: %s', str(event_data))
        action = event_data.get('action')
        action_type = event_data.get('type')

        action_event = None
        if action == 'up':
            action_event = self.on_forward
        elif action == 'down':
            action_event = self.on_backward
        elif action == 'right':
            action_event = self.on_right
        elif action == 'left':
            action_event = self.on_left

        if not action_event:
            return self.active_actions
        if action_type == 'key_down':
            self.active_actions[action] = 1
            yield from action_event(active=True)
        elif action_type == 'key_up':
            if action in self.active_actions:
                del self.active_actions[action]
                yield from action_event(active=False)
        trace_log.debug('Available keys state: %s' % self.active_actions.keys())
        return self.active_actions

    @asyncio.coroutine
    def log(self):
#        print('store_logs: %s' % self.__log_data)
        data = ','.join(map(str, self.log_data.get('dists', [0,0,0])))
        data += ',' + self.log_data.get('action', '') + "\n"
