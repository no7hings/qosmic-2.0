# coding:utf-8
# universe
from .. import abstracts as unr_abstracts


class Constant(unr_abstracts.AbsValue):
    def __init__(self, type_, raw):
        super(Constant, self).__init__(type_, raw)


class Color(unr_abstracts.AbsValue):
    def __init__(self, type_, raw):
        super(Color, self).__init__(type_, raw)


class Vector(unr_abstracts.AbsValue):
    def __init__(self, type_, raw):
        super(Vector, self).__init__(type_, raw)


class Matrix(unr_abstracts.AbsValue):
    def __init__(self, type_, raw):
        super(Matrix, self).__init__(type_, raw)


class Array(unr_abstracts.AbsValue):
    def __init__(self, type_, raw):
        super(Array, self).__init__(type_, raw)
