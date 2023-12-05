import logging
import logging.config

logger = logging.getLogger('my_logger')


class MyFilter(logging.Filter):
    def filter(self, record) -> bool:
        # print(record.__dict__)
        return True


class InfoFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if record.levelname == 'INFO':
            return True


class WarningFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if record.levelname == 'WARNING':
            return True


class ErrorFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if record.levelname == 'ERROR':
            return True


logger_config = {
    'version': 1,
    'formatters': {
        'base_msg': {
            'format': 'levelname:{levelname} msg:{msg} filename:{filename} line-number:{lineno} funcName:{funcName}',
            'style': '{',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'base_msg',
        },
        'file_info': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'base_msg',
            'filename': 'logging_file/info.log',
            'filters': ['info_filter'],
        },
        'file_warning': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'base_msg',
            'filename': 'logging_file/warning.log',
            'filters': ['warning_filter'],
        },
        'file_error': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'base_msg',
            'filename': 'logging_file/error.log',
            'filters': ['error_filter'],
        },
    },
    'filters': {
        'my_filter': {
            '()': MyFilter,
        },
        'info_filter': {
            '()': InfoFilter,
        },
        'warning_filter': {
            '()': WarningFilter,
        },
        'error_filter': {
            '()': ErrorFilter,
        },
    },
    'loggers': {
        'my_logger': {
            'level': 'INFO',
            'handlers': ['console', 'file_info', 'file_warning', 'file_error',],
            'filters': ['my_filter',],
        },
    },
}

logging.config.dictConfig(logger_config)