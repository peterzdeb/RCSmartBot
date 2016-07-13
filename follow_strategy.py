import asyncio


class StickyDistFollower(object):

    def __init__(self, event_callback):
        self.__event_callback = event_callback
        self.__log_data = {}

    def logs(self):
        print('store_logs: %s' % self.__log_data)
        data = ','.join(map(str, self.__log_data.get('dists', [0,0,0])))
        data += ',' + self.__log_data.get('action', '')
        return data

    @asyncio.coroutine
    def process_distances(self, distances):
        self.__log_data = {}
        min_dist = min(distances)
        max_dist = max(distances)
        print('process_dists: %s' % distances)
        print('min %s' % min_dist)
        if min_dist < 0.1:
            print('callback')
            self.__event_callback(action='stop')
            self.__log_data['action'] = 'stoped'
        elif min_dist < 0.6:
            print('start follow')
            yield from self.__start_following(distances)
        print("finish proc dists")
        self.__log_data['dists'] = distances

    @asyncio.coroutine
    def __start_following(self, distances):
        print('start following')
        if distances[0] > distances[1]:
            yield from self.__turn_left()
        elif distances[-1] > distances[1]:
            yield from self.__turn_right()
        else:
            yield from self.__move_forward()

    @asyncio.coroutine
    def __move_forward(self):
        self.__log_data['action'] = 'up_start'
        self.__event_callback(action='up', type='key_down')
        asyncio.sleep(0.3)
        self.__event_callback(action='up', type='key_up')
        self.__log_data['action'] = 'up_end'

    @asyncio.coroutine
    def __turn_left(self):
        self.__log_data['action'] = 'left_start'
        self.__event_callback(action='left', type='key_down')
        asyncio.sleep(0.3)
        self.__event_callback(action='left', type='key_up')
        self.__log_data['action'] = 'left_end'

    @asyncio.coroutine
    def __turn_right(self):
        self.__log_data['action'] = 'right_start'
        self.__event_callback(action='right', type='key_down')
        asyncio.sleep(0.3)
        self.__event_callback(action='right', type='key_up')
        self.__log_data['action'] = 'right_end'
