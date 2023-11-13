from utils.cli import cli
from utils.conf.config import load_config
from utils.logging.logs import init_logger

if __name__ == "__main__":
    logger = init_logger()
    logger.debug("init logger")
    cli_dict = cli.get_cli_options(standalone_mode=False)
    logger.debug("get CLI kwargs")
    settings = load_config(cli_dict["settings_file_path"], cli_dict["env"])