# coding:utf-8
import lxcontent.core as ctt_core

c = ctt_core.Content(
    value='/data/e/myworkspace/td/lynxi/script/configure/katana/script/macro/workspace.yml'
)
c.do_flatten()
print c.get_all_leaf_key_as_dag_paths()
# print c
