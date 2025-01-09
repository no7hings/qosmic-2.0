# coding:utf-8

a = dict(a='test')


class A(object):
    def __call__(self):
        return a


print '{a}'.format(**A())
