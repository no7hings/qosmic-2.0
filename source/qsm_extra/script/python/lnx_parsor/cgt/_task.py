# coding:utf-8
from ..core import base as _cor_base

from . import _base


class Task(_base.AbsTask):
    Type = _cor_base.EntityTypes.Task
    VariantKey = _cor_base.EntityVariantKeys.Task

    def __init__(self, *args, **kwargs):
        super(Task, self).__init__(*args, **kwargs)
