# coding:utf-8
import sys

import subprocess


def get_file_owner_powershell(file_path):
    try:
        # 构造 PowerShell 命令
        command = [
            "powershell",
            "-Command",
            "(Get-Acl '{0}').Owner".format(file_path)
        ]
        # 调用 PowerShell 命令获取所有者
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        # 解码输出为 Unicode 字符串
        owner = output.decode('gbk').strip()
        return owner
    except subprocess.CalledProcessError as e:
        sys.stderr.write('Error:\n')
        sys.stderr.write(e.output.decode('utf-8'))
    except Exception as e:
        sys.stderr.write('Unexpected Error:\n')
        sys.stderr.write(str(e)+'\n')
    return None

# 示例调用
file_path = r"Z:\projects\QSM_TST\source\assets\chr\lily\user.shared\cfx.cfx_rig\main\maya\scenes\lily.cfx.cfx_rig.main.v019."
owner = get_file_owner_powershell(file_path)
if owner:
    print "文件所有者:", owner
else:
    print "未能获取文件所有者"
