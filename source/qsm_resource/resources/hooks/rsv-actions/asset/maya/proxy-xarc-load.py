# coding:utf-8
file_path = session.rsv_unit.get_result(
    version='latest',
    variants_extend=dict(
        look_pass='default',
        act='static'
    )
)
if file_path:
    print file_path
