import asyncio


class BaseRobotStrategy(object):

    def __init__(self):
        self.active_actions = {}
        self.log_data = {}

    def on_stop(self):
        pass

    def on_forward(self, active=True):
        pass

    def on_backward(self, active=True):
        pass

    def on_left(self, active=True):
        pass

    def on_right(self, active=True):
        pass

    @asyncio.coroutine
    def sensor_handler(self, name, data):
        print('WARNING NotImplemented: Sensor "%s", data=%s' % (name, data))

    @asyncio.coroutine
    def event_handler(self, **event_data):
        """ Must be implemented for each strategy """
        #TODO: move into WebGamepad package
        action = event_data.get('action')
        action_type = event_data.get('type')

        action_event = lambda _: None
        if action == 'up':
            action_event = self.on_forward
        elif action == 'down':
            action_event = self.on_backward
        elif action == 'right':
            action_event = self.on_right
        elif action == 'left':
            action_event = self.on_left

        if action_type == 'key_down':
            self.active_actions[action] = 1
            yield from action_event(active=True)
        elif action_type == 'key_up':
            if action in self.active_actions:
                del self.active_actions[action]
                yield from action_event(active=False)
        print('keys: %s' % self.active_actions.keys())
        return self.active_actions

    @asyncio.coroutine
    def log(self):
#        print('store_logs: %s' % self.__log_data)
        data = ','.join(map(str, self.__log_data.get('dists', [0,0,0])))
        data += ',' + self.__log_data.get('action', '') + "\n"
        if self.__log:
            yield from self.__log.write(data)
