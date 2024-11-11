# coding:utf-8
import _base

import _asset

import _episode

import _sequence

import _shot

import _task


class Project(_base.AbsEntity):
    Type = _base.EntityTypes.Project
    VariantKey = _base.VariantKeys.Project

    NextEntitiesCacheClassDict = {
        _base.EntityTypes.Asset: _asset.AssetsCacheOpt,
        _base.EntityTypes.Episode: _episode.EpisodesCacheOpt,
        _base.EntityTypes.Sequence: _sequence.SequencesCacheOpt,
        _base.EntityTypes.Shot: _shot.ShotsCacheOpt,
    }

    TasksCacheOptClass = _task.TasksCacheOpt

    @classmethod
    def _validation_fnc(cls, variants):
        return _base.VariantKeyMatch.match_fnc(
            variants, cls.VariantKey
        )

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)

    # asset
    def find_assets(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_base.EntityTypes.Asset, variants_extend, cache_flag)

    @property
    def assets(self):
        return self.find_assets()

    def find_asset(self, name, variants_extend=None, cache_flag=True):
        return self._find_next_entity(name, _base.EntityTypes.Asset, variants_extend, cache_flag)

    def asset(self, name):
        return self.find_asset(name)

    # episode
    def find_episodes(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_base.EntityTypes.Episode, variants_extend, cache_flag)

    def episodes(self):
        return self.find_episodes()

    def find_episode(self, name, variants_extend=None, cache_flag=True):
        return self._find_next_entity(name, _base.EntityTypes.Episode, variants_extend, cache_flag)

    def episode(self, name):
        return self.find_episode(name)

    # sequence
    def find_sequences(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_base.EntityTypes.Sequence, variants_extend, cache_flag)

    @property
    def sequences(self):
        return self._find_next_entities(_base.EntityTypes.Sequence)

    def find_sequence(self, name, variants_extend=None, cache_flag=True):
        return self._find_next_entity(name, _base.EntityTypes.Sequence, variants_extend, cache_flag)

    # shot
    def find_shots(self, variants_extend=None, cache_flag=True):
        return self._find_next_entities(_base.EntityTypes.Shot, variants_extend, cache_flag)

    @property
    def shots(self):
        return self._find_next_entities(_base.EntityTypes.Shot)

    def find_shot(self, name, variants_extend=None, cache_flag=True):
        return self._find_next_entity(name, _base.EntityTypes.Shot, variants_extend, cache_flag)

    def shot(self, name):
        return self.find_shot(name)


class ProjectsCacheOpt(_base.AbsEntitiesCacheOpt):
    EntityClass = Project

    def __init__(self, *args, **kwargs):
        super(ProjectsCacheOpt, self).__init__(*args, **kwargs)

