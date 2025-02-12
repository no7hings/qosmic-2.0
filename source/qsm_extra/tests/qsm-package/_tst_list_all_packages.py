# coding:utf-8
import sys
import pkg_resources
import os
import importlib

python_paths = sys.path

# 遍历 sys.path 中的所有路径，检查每个路径下是否有包
all_packages = []

for path in python_paths:
    if os.path.isdir(path):  # 只检查目录
        # 检查路径中是否有包（如果目录下有 __init__.py 或 .dist-info 则认为是包）
        for dir_name in os.listdir(path):
            package_path = os.path.join(path, dir_name)
            if os.path.isdir(package_path):
                # 检查是否是包目录（含 __init__.py 或 .dist-info）
                if os.path.exists(os.path.join(package_path, '__init__.py')) or \
                   any(f.endswith('.dist-info') for f in os.listdir(package_path)):
                    # 获取包名称
                    package_name = dir_name.lower()
                    all_packages.append(package_name)

# 打印出未导入的包
print("Unimported packages:")
for package in all_packages:
    print(package)
