# coding:utf-8
import lxbasic.core as bsc_core


print bsc_core.PthNodeMtd.find_dag_child_paths(
    '|', ['|abc', '|abc|a'], '|'
)
