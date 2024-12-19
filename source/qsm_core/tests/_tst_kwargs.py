# coding:utf-8


def a(**kwargs):
    kwargs.pop('test')


def b(**kwargs):
    print kwargs


variants = dict(test='A')
a(**variants)
b(**variants)

