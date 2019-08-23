import sys


def config_log(server_name):
    """
    在命令行参数后面添加说明，配置log, 必须在parse_command_line()前调用
    :param server_name:
    :return:
    """
    if sys.platform == 'darwin':
        sys.argv.append(f'--log_file_prefix=./{server_name}.log')
    else:
        sys.argv.append(f'--log_file_prefix=/var/log/zhixing/{server_name}.log')

    sys.argv.append('--log_file_num_backups=4')
    sys.argv.append('--log_file_max_size=16777216')
    sys.argv.append('--logging=info')



