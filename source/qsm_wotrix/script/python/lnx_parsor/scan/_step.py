# coding:utf-8
from ..core import base as _cor_base

from . import _base


class Step(_base.AbsStep):
    Type = _cor_base.EntityTypes.Step
    VariantKey = _cor_base.EntityVariantKeys.Step

    def __init__(self, *args, **kwargs):
        super(Step, self).__init__(*args, **kwargs)
