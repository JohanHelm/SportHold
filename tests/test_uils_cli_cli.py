from click.testing import CliRunner
from utils.cli.cli import get_cli_options


def test_cli_help(cli_runner):
    result = cli_runner.invoke(get_cli_options, ["--help"])
    assert result.exit_code == 0


def test_cli_default_options(cli_runner):
    result = cli_runner.invoke(get_cli_options)
    assert result.exit_code == 0
    assert result.output == "conf\config.yaml prod INFO logs\logfile.log 10\n"
