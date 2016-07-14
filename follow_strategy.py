import asyncio


class StickyDistFollower(object):

    def __init__(self, event_callback, log=None):
        self.__event_callback = event_callback
        self.__log_data = {}
        self.__locked = False
        self.__moving = False
        self.__log = log

    @asyncio.coroutine
    def log(self):
#        print('store_logs: %s' % self.__log_data)
        data = ','.join(map(str, self.__log_data.get('dists', [0,0,0])))
        data += ',' + self.__log_data.get('action', '') + "\n"
        if self.__log:
            yield from self.__log.write(data)

    @asyncio.coroutine
    def __stop_moving(self):
        if self.__moving:
            self.__event_callback(action='down', type='key_up')
            self.__moving = False
            self.__log_data['action'] = 'down_end'


    @asyncio.coroutine
    def process_distances(self, distances):
        self.__log_data = {'dists': distances}
        min_dist = min(distances)
        max_dist = max(distances)
        print(min_dist)
        if min_dist > 1.5 or max_dist < 0.1:
            yield from self.__stop_moving()
        elif min_dist < 0.2:
            yield from self.__start_relocating(distances)
        elif min_dist < 1.5:
            yield from self.__start_following(distances)
#        print("finish proc dists")
        yield from self.log()

    @asyncio.coroutine
    def __start_relocating(self, dists):
        yield from self.__stop_moving()
        
        print("<><><><><><><><><><><><><><><>")
        if dists[0] < dists[2] and dists[2] >= 0.1:
            yield from self.__turn_left()
        elif dists[0] >= dists[2] and dists[0] >= 0.1:
            yield from self.__turn_right()

    @asyncio.coroutine
    def __start_following(self, dists):
        if dists[2] <= dists[0] and dists[1] - dists[2] > 0.05:
            yield from self.__turn_right()
        elif dists[2] > dists[0] and dists[1] - dists[0] > 0.05:
            yield from self.__turn_left()
        else:
            yield from self.__move_forward()

    @asyncio.coroutine
    def __move_forward(self):
#        if self.__locked:
#            return
        self.__log_data['action'] = 'down_start'
        self.__moving = True
        self.__event_callback(action='down', type='key_down')
        #asyncio.sleep(0.3)
        #self.__event_callback(action='up', type='key_up')

    @asyncio.coroutine
    def __turn_left(self):
        if self.__locked:
            return
        self.__log_data['action'] = 'left_start'
        yield from self.log()
        self.__locked = True
        self.__event_callback(action='left', type='key_down')
        yield from asyncio.sleep(0.15)
        self.__event_callback(action='left', type='key_up')
        self.__log_data['action'] = 'left_end'
        self.__locked = False

    @asyncio.coroutine
    def __turn_right(self):
        if self.__locked:
            return
        self.__log_data['action'] = 'right_start'
        yield from self.log()
        self.__locked = True
        self.__event_callback(action='right', type='key_down')
        yield from asyncio.sleep(0.15)
        self.__event_callback(action='right', type='key_up')
        self.__log_data['action'] = 'right_end'
        self.__locked = False
