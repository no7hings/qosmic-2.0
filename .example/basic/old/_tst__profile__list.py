# coding:utf-8
import cProfile


def test_list(list_):
    return 666666666 in list_


def test_set(set_):
    return 666666666 in set_


def test_dict(dict_):
    return 666666666 in dict_


c = 10000000


list__ = range(c)

set__ = set(range(c))

dict__ = {i: i for i in range(c)}


cProfile.run('test_list(list__)')

cProfile.run('test_set(set__)')

cProfile.run('test_dict(dict__)')
