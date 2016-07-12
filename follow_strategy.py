import asyncio


class StickyDistFollower(object):

    def __init__(self, event_callback):
        self.__event_callback = event_callback
        self.__locked = False

    @asyncio.coroutine
    def process_distances(self, distances):
        min_dist = min(distances)
        print(min_dist)
        if min_dist < 0.2 or min_dist > 0.8:
            self.__event_callback(action='down', type='key_up')
        elif min_dist < 0.8:
            yield from self.__start_following(distances)

    @asyncio.coroutine
    def __start_following(self, distances):
        if min(distances[-1], distances[1]) - distances[0] > 0.2:
            yield from self.__turn_right()
        elif min(distances[0], distances[1]) - distances[-1] > 0.2:
            yield from self.__turn_left()
        else:
            yield from self.__move_forward()

    @asyncio.coroutine
    def __move_forward(self):
#        if self.__locked:
#            return
        self.__event_callback(action='down', type='key_down')
        #asyncio.sleep(0.3)
        #self.__event_callback(action='up', type='key_up')

    @asyncio.coroutine
    def __turn_left(self):
        if self.__locked:
            return
        self.__locked = True
        self.__event_callback(action='left', type='key_down')
        yield from asyncio.sleep(0.2)
        self.__event_callback(action='left', type='key_up')
        self.__locked = False

    @asyncio.coroutine
    def __turn_right(self):
        if self.__locked:
            return
        self.__locked = True
        self.__event_callback(action='right', type='key_down')
        yield from asyncio.sleep(0.2)
        self.__event_callback(action='right', type='key_up')
        self.__locked = False
