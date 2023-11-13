import sys
from loguru import logger

def init_logger():
    logger.remove(0)
    logger.add(sys.stdout)
    return logger

