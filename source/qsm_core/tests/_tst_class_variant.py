# coding:utf-8


class B:
    class B:
        Key = 'B'


class A:
    class B:
        Key = 'A'

    def __init__(self):
        self.B = B().B


print A().B.Key
