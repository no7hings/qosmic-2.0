# coding:utf-8


class A(object):
    def __init__(self):
        pass

    def _test(self):
        print "AAA"

    def __test(self):
        print "AAA"

    def test_1(self):
        self._test()

    def test_2(self):
        self.__test()


class B(A):
    def __init__(self):
        super(B, self).__init__()

    def _test(self):
        print 'BBB'

    def __test(self):
        print 'BBB'

    # def test_2(self):
    #     self.__test()


B().test_1()
B().test_2()



