# coding:utf-8
import lxgui.core as c

h = c.GuiHistoryStage()

print(h)

h.set_one('test_0', 'test')
print(h.get_one('test_0'))

h.set_array('test_1', ['a', 'b', 'c'])
print(h.get_array('test_1'))

h.append('test_1', 'a')
print(h.get_array('test_1'))

h.extend('test_1', ['a', 'b', 'd', 'e'])
print(h.get_array('test_1'))

print(h.get_all('test_1'))
print(h.get_latest('test_1'))

h.set_one(['test', 'test_a', 'test_b.c'], 'A')
print(h.get_one(['test', 'test_a', 'test_b.c']))

