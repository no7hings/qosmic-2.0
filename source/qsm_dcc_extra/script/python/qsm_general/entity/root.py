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
        self._entity_stack = _base.EntityStack()
        super(Root, self).__init__(
            self._entity_stack, '/', dict(root=root)
        )
        
    def stack(self):
        return 

    @property
    def projects(self):
        return self.get_next_entities(self.Types.Project)

    def project(self, name):
        return self.get_next_entity(name, self.Types.Project)
