# coding:utf-8
from ..core import base as _cor_base

from . import _base


class User(_base.AbsEntity):
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
    
    @property
    def group_name(self):
        return 'no group'

    @property
    def department_name(self):
        return 'no department'
