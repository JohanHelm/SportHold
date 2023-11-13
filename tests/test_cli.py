from utils.cli.cli import get_cli_options

# TODO: rewrite with (standalone = True) in click, returned dict
def test_cli_help(cli_runner):
    result = cli_runner.invoke(get_cli_options, ["--help"])
    assert result.exit_code == 0

# TODO: rewrite with (standalone = True) in click, returned dict
def test_cli_default_options(cli_runner):
    result = cli_runner.invoke(get_cli_options)
    assert result.exit_code == 0
    assert result.output == "conf\config.yaml prod INFO logs\logfile.log 10\n"

# TODO: rewrite with (standalone = True) in click, returned dict
def test_cli_env_options(set_env, cli_runner):
    result = cli_runner.invoke(get_cli_options)
    assert result.exit_code == 0
    assert result.output == "conf\config.yaml DEV DEBUG logs\logfile.log 10\n"

# TODO: rewrite with (standalone = True) in click, returned dict
def test_cli_custom_options(cli_runner):
    result = cli_runner.invoke(
        get_cli_options,
        [
            "--settings_file_path","./conf/config.yaml",
            "--env","DEV",
            "-ll","INFO","-lf","./logs/dev_log.log",
            "-lm","10",
        ],
    )
    assert result.exit_code == 0
    assert result.output == "conf\config.yaml DEV INFO logs\dev_log.log 10\n"
