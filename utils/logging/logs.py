import sys
from loguru import logger

def init_logger():
    logger.remove(0)
    logger.add(sys.stdout)
    logger.debug("basic init logger")
    return logger

def configure_logger(logger, file_path, rotation):
    logger.add(file_path, rotation=f"{rotation} MB") 
    logger.debug(f"basic logger conf with {file_path} and rotation MB {rotation}")