# coding:utf-8
import lxbasic.core as bsc_core

c = ''.join(
    map(
        lambda x: '{}: {}\n'.format(str(x[0]).rjust(16), x[1]),
        [
            ('Name', '{name}'),
            ('ID', '{id}'),
            ('User', '{user}'),
            ('Type', '{version_type}'),
            ('Folder', '{folder}'),
            ('Review', '{review}'),
            ('Description', '{description}')
        ]
    )
)

print c
