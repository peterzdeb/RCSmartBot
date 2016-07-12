import asyncio


class StickyDistFollower(object):

    def __init__(self, event_callback):
        self.__event_callback = event_callback

    @asyncio.coroutine
    def process_distances(self, *distances):
        min_dist = min(distances)
        max_dist = max(distances)
        if min_dist < 0.1:
            self.__event_callback(action='stop')
        elif min_dist < 0.6:
            yield from self.__start_following(distances)

    @asyncio.coroutine
    def __start_following(self, distances):
        if distances[0] > distances[1]:
            yield from self.__turn_left()
        elif distances[-1] > distances[1]:
            yield from self.__turn_right()
        else:
            yield from self.__move_forward()

    @asyncio.coroutine
    def __move_forward(self):
        self.__event_callback(action='up', type='key_down')
        asyncio.sleep(0.3)
        self.__event_callback(action='up', type='key_up')

    @asyncio.coroutine
    def __turn_left(self):
        self.__event_callback(action='left', type='key_down')
        asyncio.sleep(0.3)
        self.__event_callback(action='left', type='key_up')

    @asyncio.coroutine
    def __turn_right(self):
        self.__event_callback(action='right', type='key_down')
        asyncio.sleep(0.3)
        self.__event_callback(action='right', type='key_up')
