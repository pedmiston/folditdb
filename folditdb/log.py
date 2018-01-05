import logging

logger = logging.getLogger('folditdb')

def use_logging(log_filepath='folditdb-errors.log'):
    handler = logging.FileHandler(log_filepath)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
