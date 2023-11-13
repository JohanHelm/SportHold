from utils.cli import cli
from utils.conf.config import SettingsLoader
from utils.logging.logs import init_logger, configure_logger
import asyncio
from app.telegram.bot import start_bot

if __name__ == "__main__":
    logger = init_logger()
    cli_dict = cli.get_cli_options(standalone_mode=False)
    SettingsLoader.load_settings(cli_dict["settings_file_path"], cli_dict["env"])
    settings = SettingsLoader.settings
    configure_logger(logger, cli_dict["logfile"], cli_dict["logfilemaxsize"])

    asyncio.run(start_bot())
