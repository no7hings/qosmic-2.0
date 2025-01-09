# coding:utf-8
from contextlib import contextmanager


class A(object):
    def __init__(self):
        self.start()

    def start(self):
        print 'start'

    def update(self, text):
        print 'update: {}'.format(text)

    def stop(self):
        print 'stop'


@contextmanager
def a():
    a_ = A()
    yield a_
    a_.stop()


with a() as a:
    for i in range(10):
        a.update(str(i))
