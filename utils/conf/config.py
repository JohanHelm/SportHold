from dynaconf import Dynaconf
from loguru import logger


def load_config(path_settings: str, current_env: str) -> Dynaconf:
    settings: Dynaconf = Dynaconf(
        settings_files=[path_settings],
        environments = True,
        env = current_env 
    )
    logger.debug(f"get settings from file: {path_settings} with ENV = {current_env}")
    return settings

