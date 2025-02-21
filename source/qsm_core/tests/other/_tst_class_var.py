# coding:utf-8

class A(object):
    VAR = 0

    def __init__(self):
        pass


a = A()

b = A()
b.VAR = 1

print a.VAR
print b.VAR

A.VAR = 2

print a.VAR
print b.VAR
