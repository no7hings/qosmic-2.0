# coding:utf-8
import lxbasic.content as bsc_content


print bsc_content.ToString(
    {
        'dict_0': {
            'list': [
                'A', 1, True,
            ]
        },
        '字典': {
            'list': [
                '字符', 1, True,
            ]
        },
        'list': [
            'A', 1, True,
        ],
        'tuple_empty': (),
        'tuple': ('A', 1, True,),
        'list_empty': [],
        'dict_empty': {},
        'int': 1,
        'float': 1.0,
        'str': 'c',
        'bool': True,
    }
).generate()

print bsc_content.ToString(
    [
        'A', 1, True,
    ]
).generate()

print bsc_content.ToString(
    []
).generate()
