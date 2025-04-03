# coding:utf-8
from ..core import base as _cor_base

from . import _base

from . import _project


class Root(_base.AbsEntity):
    LOG_KEY = 'scan root'

    Type = _base.EntityTypes.Root
    VariantKey = 'root'

    NextEntitiesCacheClassDict = {
        _base.EntityTypes.Project: _project.ProjectsGenerator
    }

    def __init__(self, root='X:'):
        # create before super
        self._root_entity_stack = _cor_base.EntityStack()

        super(Root, self).__init__(
            self, '/', dict(root=root)
        )

    @property
    def entity_stack(self):
        return self._root_entity_stack

    def find_projects(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_base.EntityTypes.Project, variants_extend, cache_flag)

    def projects(self, **kwargs):
        return self.find_projects(variants_extend=kwargs)

    def find_project(self, name, variants_extend=None, cache_flag=True):
        return self._find_next_entity(name, _base.EntityTypes.Project, variants_extend, cache_flag)

    def project(self, name, **kwargs):
        return self.find_project(name, variants_extend=kwargs)

    def get_entity(self, path):
        return self._root_entity_stack.get(path)
