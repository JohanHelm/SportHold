from click.testing import CliRunner

from utils.cli.cli import get_cli_options


# В своей системе создал переменные среды для тестов
# PROD=some:temp:prod:.
# DEV=some:temp:dev:.
# TEST=some:temp:test:.
def test_get_cli_with_default_options():
    runner = CliRunner()
    result = runner.invoke(get_cli_options)
    assert result.exit_code == 0
    assert result.output == 'conf/config.yaml\n' \
                            'some:temp:prod:.\n' \
                            'INFO\n' \
                            'logs/logfile.log\n' \
                            '10\n'

def test_get_cli_with_custom_options():
    runner = CliRunner()
    result = runner.invoke(get_cli_options, ('-e', 'test', '-ll', 'WARNING', '-lm', '25'))
    assert result.exit_code == 0
    assert result.output == 'conf/config.yaml\n' \
                            'some:temp:test:.\n' \
                            'WARNING\n' \
                            'logs/logfile.log\n' \
                            '25\n'
