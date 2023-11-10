from utils.logging.logging_config import make_logger
from pathlib import Path

current_catalog = Path.cwd()
# project_catalog = current_catalog.parent
project_catalog = Path.cwd()


def write_some_log():
    make_logger(f'{project_catalog}/logs/{Path(__file__)}.log', 'DEBUG').debug('Error message')
    # logger2.info('Information message')
    # logger3.warning('Warning message')


