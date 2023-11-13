from utils.cli import cli
from utils.conf.config import load_config
from utils.logging.logs import init_logger, configure_logger

if __name__ == "__main__":
    logger = init_logger()
    cli_dict = cli.get_cli_options(standalone_mode=False)
    settings = load_config(cli_dict["settings_file_path"], cli_dict["env"])
    configure_logger(logger, cli_dict["logfile"], cli_dict["logfilemaxsize"])