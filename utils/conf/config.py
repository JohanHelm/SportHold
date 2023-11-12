from pathlib import Path

from dynaconf import Dynaconf, Validator


def load_config(path_settings: str = "settings.toml",
                path_secrets: str = ".secrets.toml") -> Dynaconf:
    path_settings_exists: bool = Path(path_settings).exists()
    path_secrets_exists: bool = Path(path_secrets).exists()

    if not path_settings_exists or not path_secrets_exists:
        raise OSError("The path for the conf is incorrect")

    settings: Dynaconf = Dynaconf(
        envvar="LOYLEDUCK",
        settings_files=[path_settings, path_secrets]
    )

    settings.validators.register(
        validators=[Validator(names="BOT_TOKEN", must_exist=True),
                    Validator(names="ADMIN_IDS", is_type_of=list, must_exist=False)]
    )

    settings.validators.validate()

    return settings


def get_url(settings: Dynaconf) -> str:
    password = settings.POSTGRES_PASSWORD
    db = settings.POSTGRES_DB
    host = settings.POSTGRES_HOST
    port = settings.POSTGRES_PORT
    user = settings.POSTGRES_USER

    url: str = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

    return url
