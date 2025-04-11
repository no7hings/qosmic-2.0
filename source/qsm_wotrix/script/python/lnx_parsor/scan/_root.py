# coding:utf-8
import lxbasic.core as bsc_core

from ..core import base as _cor_base

from . import _base

from . import _people

from . import _project


class Root(_base.AbsEntity):
    LOG_KEY = 'scan root'

    Type = _cor_base.EntityTypes.Root
    VariantKey = 'root'

    NextEntitiesGeneratorClsDict = {
        _cor_base.EntityTypes.Project: _project.ProjectsGenerator
    }

    def __init__(self, stage, location='X:'):
        self._stage = stage

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

    def current_user(self):
        return None

    def users(self, **kwargs):
        return []

    def user(self, name, **kwargs):
        return None

    @_base.EntityFactory.find_all(_cor_base.EntityTypes.Project)
    def projects(self, **kwargs):
        pass

    @_base.EntityFactory.find_one(_cor_base.EntityTypes.Project)
    def project(self, name, **kwargs):
        pass
