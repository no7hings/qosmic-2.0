# coding:utf-8
import lxbasic.content as bsc_content

d = {
    'option': {
        'x': 1,
        'asset_name': 'abc',
    },
    'root': '|<option.asset_name>',
    'x': '=(<option.x> + 2)*5'
}

c = bsc_content.Content(None, d)
c.set('asset_name', 'cc')
c.do_flatten()

print c.get('root')
print c.get('x')

print c
