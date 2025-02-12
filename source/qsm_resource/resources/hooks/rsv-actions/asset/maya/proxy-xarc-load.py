# coding:utf-8
from __future__ import print_function

file_path = session.rsv_unit.get_result(
    version='latest',
    variants_extend=dict(
        look_pass='default',
        act='static'
    )
)
if file_path:
    print(file_path)
