# coding:utf-8
import sys

from . import base as _base

from . import project as _project


class Root(_base.AbsEntity):
    LOG_KEY = 'scan root'

    Type = _base.EntityTypes.Root
    VariantKey = 'root'

    NextEntityQueryClassDict = {
        _base.EntityTypes.Project: _project.ProjectsCache
    }

    ROOT = None

    ROOT_DICT = dict()

    def __init__(self, root=None):
        self._root_entity_stack = _base.NodeStack()
        super(Root, self).__init__(
            self, '/', dict(root=root)
        )

    def __new__(cls, *args, **kwargs):
        root = kwargs.get('root', 'X:')
        if root in cls.ROOT_DICT:
            return cls.ROOT_DICT[root]

        instance = super(Root, cls).__new__(cls, root=root)
        cls.ROOT_DICT[root] = instance
        sys.stdout.write('new scan root: "{}"\n'.format(root))
        return instance

    @property
    def entity_stack(self):
        return self._root_entity_stack

    @property
    def projects(self):
        return self.get_next_entities(_base.EntityTypes.Project)

    def project(self, name):
        return self.get_next_entity(name, _base.EntityTypes.Project)

    def get_entity(self, path):
        return self._root_entity_stack.get(path)

    def find_one(self, entity_type, filters):
        pass

    def find_all(self, entity_type, filters):
        pass

    @classmethod
    def generate(cls):
        if cls.ROOT is not None:
            return cls.ROOT
        _ = cls(root='X:')
        cls.ROOT = _
        return _
