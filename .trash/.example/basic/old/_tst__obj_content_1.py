# coding:utf-8
import lxbasic.content as bsc_content

c = bsc_content.Content(
    value='/data/e/myworkspace/td/lynxi/script/configure/katana/script/macro/workspace.yml'
)
c.do_flatten()
print c.get_all_leaf_key_as_dag_paths()
# print c
