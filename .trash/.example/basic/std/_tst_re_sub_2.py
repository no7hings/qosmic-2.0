# coding:utf-8
import re

def replace_ampersand(match):
    if match.group(1):
        return match.group(0)
    else:
        return '^&'

# 定义你的命令行字符串
command_line = r'test_0 && test_1 -o "\"application=maya&asset=td_test&project=nsa_dev&scheme=asset-task&task=surfacing&task_id=202455\"" -c application=maya&asset=td_test&project=nsa_dev'

# 使用正则表达式替换不在引号内和不在"&&"之后的&
modified_command_line = re.sub(r'(("[^"]*")|&&|[^&])(&)([^&]|&&|$)', lambda x: x.group(0) if x.group(1) else '^&', command_line)

print modified_command_line
