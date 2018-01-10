import logging

logger = logging.getLogger('folditdb')

def use_logging(log_filepath='folditdb.log'):
    handler = logging.FileHandler(log_filepath)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.ERROR)
