# coding:utf-8


class A(object):
    def __init__(self):
        pass

    def a(self):
        print 'c'


a = A()

print a.__getattribute__('a')
