# from utils.cli.cli import get_cli_options
#
#
# def test_cli_help(cli_runner):
#     result = cli_runner.invoke(get_cli_options, ["--help"])
#     assert result.exit_code == 0
#
#
# def test_cli_default_options(cli_runner):
#     result = cli_runner.invoke(get_cli_options)
#     assert result.exit_code == 0
#
#
# def test_cli_env_options(set_env, cli_runner):
#     result = cli_runner.invoke(get_cli_options)
#     assert result.exit_code == 0
#
#
# def test_cli_custom_options(cli_runner):
#     result = cli_runner.invoke(
#         get_cli_options,
#         [
#             "--settings_file_path",
#             "./conf/config.yaml",
#             "--env",
#             "DEVELOPMENT",
#             "-ll",
#             "INFO",
#             "-lf",
#             "./logs/dev_log.log",
#             "-lm",
#             "10",
#         ],
#     )
#     assert result.exit_code == 0
#
# def test_cli_bad_custom_options(cli_runner):
#     result = cli_runner.invoke(
#         get_cli_options,
#         [
#             "--settings_file_path",
#             "./conf/config.yaml",
#             "--env",
#             "DEV", # error option
#             "-ll",
#             "INFO",
#             "-lf",
#             "./logs/dev_log.log",
#             "-lm",
#             "10",
#         ],
#     )
#     assert result.exit_code == 2