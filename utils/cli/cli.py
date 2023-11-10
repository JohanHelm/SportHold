from pathlib import Path
import click

ENVS = ["prod","dev", "test"]

@click.command()
# если параметр не передан напрямую взять его из переменных среды (envvar)
# проверка на то, что введеной значение есть 'Path'
@click.option(
    "-s",
    "--settings_file_path",
    default="./conf/config.yaml", 
    help="Path to config file.",
    type=Path,
    show_default=True,
)
# тут же делать проверку https://click.palletsprojects.com/en/8.1.x/options/#choice-options
# если параметр не передан напрямую взять его из переменных среды (envvar)
@click.option(
    "-e",
    "--env",
    type=str,
    default="production",
    show_default=True,
    help="Choose one of next options: production, test, development",
)

# @cick.option(-ll --loglevel уровень логирования -- DEBUG, INFO ...)
# @cick.option(-lf --logfile путь к файлу для логировани -- Path)
# @cick.option(-lm --logfilemaxsize ограничение на рамер лог файла по исчерпанию которого файл ротируется -- Path)

# def get_options(settings: str, env: str):
def get_cli_options(settings_file_path: Path, 
                    env: ENVS,
                    loglevel,
                    logfile,
                    logfilemaxsize): # ENVS - проверить TypeHints
    
    # return 

    # тут будем передавать данные в Dynaconf
    # options = []
    # if Path(settings).exists():
    #     options.append(settings)
    #     click.echo(f"Config file {settings} really exists!")
    # else:
    #     click.echo(f"Config file {settings} not found!")

    # if env in ("production", "test", "development"):
    #     options.append(env)
    #     click.echo(f'Choosen environmet "{env}" can be applied!')
    # else:
    #     click.echo(f"You have to choose one of: production, test, development!")

    # if len(options) == 2:
    #     cli_builder(options)


# 1. Путь к конфиг файлу. -s --settings
# 2. Какой енв брать из конфигурационного файла. -e --environment (production, test, development)
# 3. парамтры логгирования из командной строки или из конфиг файла


def cli_builder(options):
    print("build cli application")
