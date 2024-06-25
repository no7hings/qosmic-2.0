# coding:utf-8
from . import base as _base


class LocatorNodeOpt(_base.AbsNodeOpt):
    TYPE_INCLUDES = [
        'nucleus',

        'airField',
        'dragField',
        'gravityField',
        'newtonField',
        'radialField',
        'turbulenceField',
        'uniformField',
        'vortexField',
    ]

    SCHEME_BASE = '/xform'

    def __init__(self, *args, **kwargs):
        super(LocatorNodeOpt, self).__init__(*args, **kwargs)
