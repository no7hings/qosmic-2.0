# coding:utf-8
from . import base as _base

from . import task as _task

from . import asset as _asset

from . import sequence as _sequence

from . import shot as _shot


class Project(_base.AbsEntity):
    Type = _base.EntityTypes.Project
    VariantKey = _base.VariantKeys.Project

    NextEntityQueryClassDict = {
        _base.EntityTypes.Asset: _asset.AssetsCache,
        _base.EntityTypes.Sequence: _sequence.SequencesCache,
        _base.EntityTypes.Shot: _shot.ShotsCache,
    }

    TaskQueryClass = _task.TasksCache

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)

    def find_assets(self, variants_extend=None):
        return self.get_next_entities(_base.EntityTypes.Asset, variants_extend)
    
    @property
    def assets(self):
        return self.get_next_entities(_base.EntityTypes.Asset)

    def asset(self, name):
        return self.get_next_entity(name, _base.EntityTypes.Asset)

    @property
    def sequences(self):
        return self.get_next_entities(_base.EntityTypes.Sequence)

    @property
    def shots(self):
        return self.get_next_entities(_base.EntityTypes.Shot)


class ProjectsCache(_base.AbsEntitiesCache):
    EntityClass = Project

    def __init__(self, *args, **kwargs):
        super(ProjectsCache, self).__init__(*args, **kwargs)

