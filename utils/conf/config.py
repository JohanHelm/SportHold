from loguru import logger
from dynaconf import Dynaconf


class SettingsLoader:
    settings = None

    @classmethod
    def load_settings(cls, path_settings: str, current_env: str) -> Dynaconf:
        settings: Dynaconf = Dynaconf(
            settings_files=[path_settings], environments=True, env=current_env
        )
        logger.debug(
            f"get settings from file: {path_settings} with ENV = {current_env}"
        )
        cls.settings = settings

    @staticmethod
    def settings(cls):
        return cls.settings
