# coding:utf-8
from . import _base

from . import _role

from . import _asset

from . import _episode

from . import _sequence

from . import _shot

from . import _task


class Project(_base.AbsEntity):
    Type = _base.EntityTypes.Project
    VariantKey = _base.EntityVariantKeys.Project

    NextEntitiesCacheClassDict = {
        _base.EntityTypes.Role: _role.RolesGenerator,
        _base.EntityTypes.Asset: _asset.AssetsGenerator,
        _base.EntityTypes.Episode: _episode.EpisodesGenerator,
        _base.EntityTypes.Sequence: _sequence.SequencesGenerator,
        _base.EntityTypes.Shot: _shot.ShotsGenerator,
    }

    TasksGeneratorClass = _task.TasksGenerator

    @classmethod
    def _variant_validation_fnc(cls, variants):
        return _base.VariantKeyMatch.match_fnc(variants, cls.VariantKey)

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)

    # role
    def find_roles(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_base.EntityTypes.Role, variants_extend, cache_flag)

    # asset
    def find_assets(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_base.EntityTypes.Asset, variants_extend, cache_flag)

    def assets(self, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self.find_assets(variants_extend=kwargs, cache_flag=cache_flag)

    def find_asset(self, name, variants_extend=None, cache_flag=True):
        return self._find_next_entity(name, _base.EntityTypes.Asset, variants_extend, cache_flag)

    def asset(self, name, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self.find_asset(name, variants_extend=kwargs, cache_flag=cache_flag)

    # episode
    def find_episodes(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_base.EntityTypes.Episode, variants_extend, cache_flag)

    def episodes(self, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self.find_episodes(variants_extend=kwargs, cache_flag=cache_flag)

    def find_episode(self, name, variants_extend=None, cache_flag=True):
        return self._find_next_entity(name, _base.EntityTypes.Episode, variants_extend, cache_flag)

    def episode(self, name, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self.find_episode(name, variants_extend=kwargs, cache_flag=cache_flag)

    # sequence
    def find_sequences(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_base.EntityTypes.Sequence, variants_extend, cache_flag)

    def sequences(self, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self.find_sequences(variants_extend=kwargs, cache_flag=cache_flag)

    def find_sequence(self, name, variants_extend=None, cache_flag=True):
        return self._find_next_entity(name, _base.EntityTypes.Sequence, variants_extend, cache_flag)

    def sequence(self, name, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self.find_sequence(name, variants_extend=kwargs, cache_flag=cache_flag)

    # shot
    def find_shots(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_base.EntityTypes.Shot, variants_extend, cache_flag)

    def shots(self, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self.find_shots(variants_extend=kwargs, cache_flag=cache_flag)

    def find_shot(self, name, variants_extend=None, cache_flag=True):
        return self._find_next_entity(name, _base.EntityTypes.Shot, variants_extend, cache_flag)

    def shot(self, name, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self.find_shot(name, variants_extend=kwargs, cache_flag=cache_flag)


class ProjectsGenerator(_base.AbsEntitiesGenerator):
    EntityClass = Project

    def __init__(self, *args, **kwargs):
        super(ProjectsGenerator, self).__init__(*args, **kwargs)

