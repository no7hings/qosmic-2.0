# coding:utf-8
from ..core import base as _cor_base

from . import _base

from . import _project


class Root(_base.AbsEntity):
    LOG_KEY = 'scan root'

    Type = _cor_base.EntityTypes.Root
    VariantKey = 'root'

    NextEntitiesCacheClassDict = {
        _cor_base.EntityTypes.Project: _project.ProjectsGenerator
    }

    def __init__(self, location='X:'):
        # create before super
        self._root_entity_stack = _cor_base.EntityStack()

        super(Root, self).__init__(
            self, '/', dict(root=location)
        )

    @property
    def entity_stack(self):
        return self._root_entity_stack

    def get_entity(self, path):
        return self._root_entity_stack.get(path)

    def find_projects(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_cor_base.EntityTypes.Project, variants_extend, cache_flag)

    def projects(self, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self.find_projects(variants_extend=kwargs, cache_flag=cache_flag)

    def find_project(self, name, variants_extend=None, cache_flag=True):
        return self._find_next_entity(name, _cor_base.EntityTypes.Project, variants_extend, cache_flag)

    def project(self, name, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self.find_project(name, variants_extend=kwargs, cache_flag=cache_flag)
