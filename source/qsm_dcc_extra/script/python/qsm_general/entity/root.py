# coding:utf-8
from . import base as _base

from . import project as _project


class Root(_base.AbsEntity):
    Type = _base.EntityTypes.Root
    VariantKey = 'root'

    NextEntityQueryClassDict = {
        _base.EntityTypes.Project: _project.ProjectQuery
    }

    def __init__(self, root='X:'):
        self._root_entity_stack = _base.NodeStack()
        super(Root, self).__init__(
            self, '/', dict(root=root)
        )

    @property
    def entity_stack(self):
        return self._root_entity_stack

    @property
    def projects(self):
        return self.get_next_entities(_base.EntityTypes.Project)

    def project(self, name):
        return self.get_next_entity(name, _base.EntityTypes.Project)

    def get_one(self, entity_type, filters):
        pass

    def get_all(self, entity_type, filters):
        pass
