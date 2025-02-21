# coding:utf-8
import functools


def test_fnc(entity_type, name):
    print entity_type, name


fnc = functools.partial(test_fnc, 'Test')

print fnc(name='sam')
