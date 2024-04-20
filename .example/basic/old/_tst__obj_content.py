# coding:utf-8
import lxcontent.core as ctt_core

c = ctt_core.Content(value={})
print c

c.set('a', '\\<A\\>')
c.set('c', 'C')
c.set('b', '<c>')
c.set('e.a.b.c', '<c>')
print c

c.do_flatten()
print c
print c['b']
print c.get('b')

c.set('e.a.b.c', 'e')
print c
