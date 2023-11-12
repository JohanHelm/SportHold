# # from utils.logging.logging_config import make_logger
# # from pathlib import Path

# # current_catalog = Path.cwd()
# # # project_catalog = current_catalog.parent
# # project_catalog = Path.cwd()


# # def write_some_log():
# #     make_logger(f'{project_catalog}/logs/{Path(__file__)}.log', 'DEBUG').debug('Error message')
# #     # logger2.info('Information message')
# #     # logger3.warning('Warning message')


# from os import name
# from pathlib import Path
# import click

# ENVS = ["prod", "dev", "test"]


# @click.command()
# @click.option(
#     "-s",
#     "--settings_file_path",
#     default="./conf/config.yaml",
#     help="Path to config file.",
#     type=Path,
#     show_default=True,
# )
# @click.option(
#     "-e",
#     "--env",
#     type=str,
#     default="production",
#     show_default=True,
#     help="Choose one of next options: production, test, development",
# )
# def app_builder(settings_file_path: str, env: str):
#     print(123)

import click


@click.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    return (count, name)


if __name__ == "__main__":
    count, name = hello()
    print(count, name)
