# coding:utf-8


class A(object):
    def __init__(self):
        pass

    def get_type(self):
        raise NotImplementedError()

    type = property(get_type)


class B(A):
    def __init__(self):
        super(B, self).__init__()

    def get_type(self):
        return 'ccc'


if __name__ == '__main__':
    print B().type
