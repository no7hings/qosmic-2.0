# coding:utf-8
import subprocess


def find_process_path_by_name(name):
    try:
        output = subprocess.check_output(
            'wmic process where "name=\'{name}\'" get ExecutablePath'.format(name=name),
            shell=True
        ).decode('utf-8', errors='ignore').splitlines()
        paths = [line.strip() for line in output if line.strip() and 'ExecutablePath' not in line]
        return list(set(paths))
    except subprocess.CalledProcessError:
        return []

# 示例：查找 notepad.exe 的路径
for path in find_process_path_by_name("GitHubDesktop.exe"):
    print(path)
