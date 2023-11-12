from pathlib import Path
import click
import os


@click.command()
# если параметр не передан напрямую взять его из переменных среды (envvar)
# проверка на то, что введеной значение есть 'Path'
@click.option(
    "-s",
    "--settings_file_path",
    type=click.Path(
        exists=True,
        readable=True,
        resolve_path=False,
        path_type=Path,
    ),
    default="./conf/config.yaml",
    show_default=True,
    help="Path to config file.",
    envvar="SETTING_FILE_PATH",
)
# тут же делать проверку https://click.palletsprojects.com/en/8.1.x/options/#choice-options
# если параметр не передан напрямую взять его из переменных среды (envvar)
@click.option(
    "-e",
    "--env",
    type=click.Choice(("prod", "dev", "test"), case_sensitive=False),
    default="prod",
    show_default=True,
    help="Choose one of environment variables: prod, test, dev",
    envvar="ENV",
)
@click.option(  #  уровень логирования -- DEBUG, INFO ...
    "-ll",
    "--loglevel",
    type=click.Choice(("DEBUG", "INFO", "WARNING"), case_sensitive=False),
    default="INFO",
    show_default=True,
    help="Choose logging level",
    envvar="LOGLEVEL",
)
@click.option(  #  путь к файлу для логировани -- Path
    "-lf",
    "--logfile",
    type=click.Path(
        exists=False,  # файл создает сам логгер
        writable=True,
        resolve_path=False,
        path_type=Path,
    ),
    default="./logs/logfile.log",
    show_default=True,
    help="Path to log file.",
    envvar="LOGFILE",
)
@click.option(  #  ограничение на рамер лог файла по исчерпанию которого файл ротируется -- Path
    "-lm",
    "--logfilemaxsize",
    type=click.INT,  # ore click.STR, 10M for example
    default=10,
    show_default=True,
    help="Max size of log file before rotation in megabytes.",
    envvar="LOGFILEMAXSIZE",
)
def get_cli_options(
    settings_file_path: Path, env: str, loglevel: str, logfile: str, logfilemaxsize: int
):  # ENVS - проверить TypeHints
    print(
        settings_file_path,
        env,
        loglevel,
        logfile,
        logfilemaxsize
        )


def cli_builder(options):
    print("build cli application")
