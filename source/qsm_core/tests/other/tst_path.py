# coding:utf-8
from __future__ import print_function

import lxbasic.core as bsc_core


print(bsc_core.BscNodePath.find_dag_child_paths(
    '|', ['|abc', '|abc|a'], '|'
))
