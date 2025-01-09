# coding:utf-8
import sys


def test(a, b):
    print sys._getframe().f_code.co_name
    print sys._getframe().f_code.co_varnames
    print sys._getframe().f_code.co_filename


test("a", "b")
