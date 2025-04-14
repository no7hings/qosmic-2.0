# coding:utf-8
from ..core import base as _cor_base

from . import _base


class Department(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Department
    VariantKey = _cor_base.EntityVariantKeys.Department

    def __init__(self, *args, **kwargs):
        super(Department, self).__init__(*args, **kwargs)


class User(_base.AbsEntity):
    Type = _cor_base.EntityTypes.User
    VariantKey = _cor_base.EntityVariantKeys.User

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    @property
    def group_name(self):
        return self._dtb_variants.get('account.group')

    @property
    def department_name(self):
        return self._dtb_variants.get('account.department')

    def all_project_tasks(self, **kwargs):
        return []

    def all_asset_tasks(self, **kwargs):
        return []
