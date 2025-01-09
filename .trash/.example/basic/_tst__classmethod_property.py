# coding:utf-8
import time


class A(object):
    Abc = None

    class __metaclass__(type):
        @property
        def Abc(cls):
            return 'aaa'


class ClassProperty(property):
    def __get__(self, cls, objtype=None):
        return super(ClassProperty, self).__get__(objtype)

    def __set__(self, cls, value):
        super(ClassProperty, self).__set__(type(cls), value)

    def __delete__(self, cls):
        super(ClassProperty, self).__delete__(type(cls))


class B(object):

    @ClassProperty
    def Abc(cls):
        return time.time()


print B.Abc
