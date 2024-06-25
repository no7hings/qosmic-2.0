# coding:utf-8
from . import base as _base


class AnyNodeOpt(_base.AbsNodeOpt):
    TYPE_INCLUDES = []

    def __init__(self, *args, **kwargs):
        super(AnyNodeOpt, self).__init__(*args, **kwargs)


class AnyShapeOpt(_base.AbsShapeOpt):
    def __init__(self, *args, **kwargs):
        super(AnyShapeOpt, self).__init__(*args, **kwargs)
