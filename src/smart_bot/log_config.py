import logging
from logging.config import dictConfig
import os


APP_LOG_LEVEL = logging.DEBUG
OTHERS_LOG_LEVEL = logging.INFO
TRACE_LOG_LEVEL = logging.INFO

LOG_DIR = os.path.join(os.getcwd(), 'logs')

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'handlers': ['console', 'default'],
    },
    'formatters': {
        'default': {
            'format': '%(asctime)s %(name)s %(levelname)s %(module)s.%(funcName)s %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default',
        },
        'default': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.getLevelName(OTHERS_LOG_LEVEL),
            'filename': os.path.join(LOG_DIR, 'robot_modules.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 10,
            'formatter': 'default',
        },
        'smart_bot': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'smart_robot.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 10,
            'formatter': 'default',
        },
    },
    'loggers': {
        'smart_bot': {
            'handlers': ['smart_bot', 'console'],
            'propagate': False,
            'level': APP_LOG_LEVEL
        },
        'smart_bot.trace': {
            'handlers': ['smart_bot', 'console'],
            'propagate': False,
            'level': TRACE_LOG_LEVEL
        },
        'web_gamepad': {
            'handlers': ['smart_bot', 'console'],
            'propagate': False,
            'level': APP_LOG_LEVEL
        },
        'asyncio': {
            'handlers': ['smart_bot', 'console'],
            'propagate': False,
            'level': APP_LOG_LEVEL
        },
    }
}


def setup_loggers():
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)
    logging.config.dictConfig(LOG_CONFIG)
