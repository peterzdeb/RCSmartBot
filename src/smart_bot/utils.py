import builtins
import logging
import sys

trace_log = logging.getLogger('smart_bot.trace')

def trace_print(*args, **kwargs):
    caller = sys._getframe(1)
    func = caller.f_locals.get('func')
    module = caller.f_globals.get('__name__')
    if func:
        caller_name = func.__name__
    else:
        caller_name = ''
    trace_log.info('%s.%s() => %s, %s', module, caller_name, args, kwargs)

builtins.print = trace_print
