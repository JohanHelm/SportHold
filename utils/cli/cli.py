from pathlib import Path
import click
import os


@click.command()
# если параметр не передан напрямую взять его из переменных среды (envvar)
# проверка на то, что введеной значение есть 'Path'
@click.option(
    "-s",
    "--settings_file_path",
    type=click.Path(exists=True),
    default="./conf/config.yaml",
    show_default=True,
    help="Path to config file.",
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
)
@click.option(   #  уровень логирования -- DEBUG, INFO ...
    '-ll',
    '--loglevel',
    type=click.Choice(('DEBUG', 'INFO', 'WARNING'), case_sensitive=False),
    default='INFO',
    show_default=True,
    help="Choose logging level"
)
@click.option(   #  путь к файлу для логировани -- Path
    '-lf',
    '--logfile',
    type=click.Path(exists=True),
    default="./logs/logfile.log",
    show_default=True,
    help="Path to log file.",
)
@click.option(   #  ограничение на рамер лог файла по исчерпанию которого файл ротируется -- Path
    '-lm',
    '--logfilemaxsize',
    type=int,  # ore str, 10M for example
    default=10,
    show_default=True,
    help="Max size of log file before rotation.",
)
def get_cli_options(settings_file_path: Path, env: str, loglevel: str, logfile: str, logfilemaxsize: int): # ENVS - проверить TypeHints
    
    click.echo(settings_file_path)
    click.echo(os.getenv(env.upper()))  # Можно доставать переменную среды библеотеками os, environs, dotenv
    click.echo(loglevel)
    click.echo(logfile)
    click.echo(logfilemaxsize)


    # тут будем передавать данные в Dynaconf



# 1. Путь к конфиг файлу. -s --settings
# 2. Какой енв брать из конфигурационного файла. -e --environment (production, test, development)
# 3. парамтры логгирования из командной строки или из конфиг файла


def cli_builder(options):
    print("build cli application")
