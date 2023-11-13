from dynaconf import Dynaconf


def load_config(path_settings: str, current_env: str) -> Dynaconf:
    settings: Dynaconf = Dynaconf(
        settings_files=[path_settings],
        environments = True,
        env = current_env 
    )

    return settings

