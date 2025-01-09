# coding:utf-8
import functools


class A(object):
    def __init__(self, a):
        self._a = a

    def set_run(self):
        print self._a


def test_0():
    def run_fnc_():
        print i
    #
    lis = []
    #
    for i in range(10):
        lis.append(
            run_fnc_
        )

    for j in lis:
        print j
        j()


def test_1():
    def add_fnc_(i_):
        def run_fnc_():
            print i_
        #
        lis.append(
            run_fnc_
        )
    #
    lis = []
    #
    for i in range(10):
        add_fnc_(i)

    for j in lis:
        print j
        j()


def test_2():
    def run_fnc_(i_):
        print i_
    #
    lis = []
    #
    for i in range(10):
        lis.append(
            functools.partial(run_fnc_, i)
        )

    for j in lis:
        print j
        j()


test_0()
# test_1()
# test_2()
