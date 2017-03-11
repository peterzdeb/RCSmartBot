__STRATEGY = None

def get_strategy():
    return __STRATEGY

def select_strategy(strategy_class):
    global __STRATEGY
    __STRATEGY = strategy_class()
    return __STRATEGY