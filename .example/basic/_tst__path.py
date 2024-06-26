# coding:utf-8
import lxbasic.core as bsc_core


print bsc_core.BscPath.to_leaf_paths(
    ['/a', '/a/b/c', '/a/b', '/b', '/bc']
)
