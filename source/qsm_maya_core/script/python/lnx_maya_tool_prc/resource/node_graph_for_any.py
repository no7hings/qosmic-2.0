# coding:utf-8
from . import base as _base


class AnyNodeGraphOpt(_base.AbsNodeGraphOpt):
    TYPE_INCLUDES = []

    def __init__(self, *args, **kwargs):
        super(AnyNodeGraphOpt, self).__init__(*args, **kwargs)
