# coding:utf-8
from ..core import base as _cor_base

from . import _base

from . import _role

from . import _asset

from . import _episode

from . import _sequence

from . import _shot

from . import _task


class Project(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Project
    VariantKey = _base.EntityVariantKeys.Project

    NextEntitiesCacheClassDict = {
        _cor_base.EntityTypes.Role: _role.RolesGenerator,
        _cor_base.EntityTypes.Asset: _asset.AssetsGenerator,
        _cor_base.EntityTypes.Episode: _episode.EpisodesGenerator,
        _cor_base.EntityTypes.Sequence: _sequence.SequencesGenerator,
        _cor_base.EntityTypes.Shot: _shot.ShotsGenerator,
    }

    TasksGeneratorClass = _task.TasksGenerator

    @classmethod
    def _variant_validation_fnc(cls, variants):
        return _base.VariantKeyMatch.match_fnc(variants, cls.VariantKey)

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)

    # role
    def _find_roles(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_cor_base.EntityTypes.Role, variants_extend, cache_flag)

    def roles(self, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self._find_roles(variants_extend=kwargs, cache_flag=cache_flag)

    def _find_role(self, name, variants_extend=None, cache_flag=True):
        return self._find_next_entity(name, _cor_base.EntityTypes.Role, variants_extend, cache_flag)
    
    def role(self, name, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self._find_role(name, variants_extend=kwargs, cache_flag=cache_flag)

    # asset
    def _find_assets(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_cor_base.EntityTypes.Asset, variants_extend, cache_flag)

    def assets(self, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self._find_assets(variants_extend=kwargs, cache_flag=cache_flag)

    def _find_asset(self, name, variants_extend=None, cache_flag=True):
        return self._find_next_entity(name, _cor_base.EntityTypes.Asset, variants_extend, cache_flag)

    def asset(self, name, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self._find_asset(name, variants_extend=kwargs, cache_flag=cache_flag)

    # episode
    def _find_episodes(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_cor_base.EntityTypes.Episode, variants_extend, cache_flag)

    def episodes(self, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self._find_episodes(variants_extend=kwargs, cache_flag=cache_flag)

    def _find_episode(self, name, variants_extend=None, cache_flag=True):
        return self._find_next_entity(name, _cor_base.EntityTypes.Episode, variants_extend, cache_flag)

    def episode(self, name, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self._find_episode(name, variants_extend=kwargs, cache_flag=cache_flag)

    # sequence
    def _find_sequences(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_cor_base.EntityTypes.Sequence, variants_extend, cache_flag)

    def sequences(self, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self._find_sequences(variants_extend=kwargs, cache_flag=cache_flag)

    def _find_sequence(self, name, variants_extend=None, cache_flag=True):
        return self._find_next_entity(name, _cor_base.EntityTypes.Sequence, variants_extend, cache_flag)

    def sequence(self, name, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self._find_sequence(name, variants_extend=kwargs, cache_flag=cache_flag)

    # shot
    def _find_shots(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_cor_base.EntityTypes.Shot, variants_extend, cache_flag)

    def shots(self, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self._find_shots(variants_extend=kwargs, cache_flag=cache_flag)

    def _find_shot(self, name, variants_extend=None, cache_flag=True):
        return self._find_next_entity(name, _cor_base.EntityTypes.Shot, variants_extend, cache_flag)

    def shot(self, name, **kwargs):
        cache_flag = kwargs.pop('cache_flag') if 'cache_flag' in kwargs else False
        return self._find_shot(name, variants_extend=kwargs, cache_flag=cache_flag)


class ProjectsGenerator(_base.AbsEntitiesGenerator):
    EntityClass = Project

    def __init__(self, *args, **kwargs):
        super(ProjectsGenerator, self).__init__(*args, **kwargs)

