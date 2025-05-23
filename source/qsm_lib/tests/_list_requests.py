# coding:utf-8
import os

import pkg_resources

site_packages = r"E:\myworkspace\qosmic-2.0\source\qsm_katana_lib\lib\windows-python-3.10\site-packages"

env = pkg_resources.Environment([site_packages])

for project_name in env:
    for dist in env[project_name]:
        print("%s==%s" % (dist.project_name, dist.version))
        if dist.requires():
            for req in dist.requires():
                print("  - %s" % req)
