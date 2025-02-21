import logging, sys

logger = logging.getLogger('user_activity_logger')

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(logging.Formatter('%(levelname)s %(asctime)s %(message)s', style='%'))
logger.addHandler(stream_handler)

def log_event(message, level='info'):
    if level == 'info':
        logger.info(message)
    elif level == 'warning':
        logger.warning(message)
    elif level == 'error':
        logger.error(message)