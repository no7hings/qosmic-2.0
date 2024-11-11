# coding:utf-8
import _base

from . import _project as _project


class Root(_base.AbsEntity):
    LOG_KEY = 'scan root'

    Type = _base.EntityTypes.Root
    VariantKey = 'root'

    NextEntitiesCacheClassDict = {
        _base.EntityTypes.Project: _project.ProjectsCacheOpt
    }

    INSTANCE = None

    def __init__(self, root='X:'):
        self._root_entity_stack = _base.EntityStack()
        super(Root, self).__init__(
            self, '/', dict(root=root)
        )

    @property
    def entity_stack(self):
        return self._root_entity_stack

    def find_projects(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_base.EntityTypes.Project, variants_extend, cache_flag)

    @property
    def projects(self):
        return self._find_next_entities(_base.EntityTypes.Project)

    def project(self, name):
        return self._find_next_entity(name, _base.EntityTypes.Project)

    def find_project(self, name, variants_extend=None, cache_flag=True):
        return self._find_next_entity(name, _base.EntityTypes.Project, variants_extend, cache_flag)

    def find_asset(self, project, asset):
        return self.find_project(project).find_asset(asset)

    def get_entity(self, path):
        return self._root_entity_stack.get(path)

    def find_one(self, entity_type, filters):
        pass

    def find_all(self, entity_type, filters):
        pass

    @classmethod
    def generate(cls):
        if cls.INSTANCE is not None:
            return cls.INSTANCE
        _ = cls(root='X:')
        cls.INSTANCE = _
        return _
