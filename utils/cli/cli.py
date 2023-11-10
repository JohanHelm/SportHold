from pathlib import Path
import click


@click.command()
@click.option("-s", "--settings", default='config.txt', help='Path to config file.', type=str, show_default=True)
@click.option("-e", "--env", type=str, default='production', show_default=True,
              help='Choose one of next options: production, test, development')
def take_options(settings: str, env: str):
    options = []
    if Path(settings).exists():
        options.append(settings)
        click.echo(f"Config file {settings} really exists!")
    else:
        click.echo(f"Config file {settings} not found!")

    if env in ('production', 'test', 'development'):
        options.append(env)
        click.echo(f"Choosen environmet \"{env}\" can be applied!")
    else:
        click.echo(f"You have to choose one of: production, test, development!")

    if len(options) == 2:
        cli_builder(options)


# 1. Путь к конфиг файлу. -s --settings
# 2. Какой енв брать из конфигурационного файла. -e --environment (production, test, development)
# 3. парамтры логгирования из командной строки или из конфиг файла


def cli_builder(options):
    print('build cli application')
