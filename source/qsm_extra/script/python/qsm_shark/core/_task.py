# coding:utf-8
import sys

import copy

import _base

import _abc


class _ResourceTask(_abc.AbsEntity):
    EntityType = _base.EntityTypes.Task
    VariantKey = _base.VariantKeys.Task

    @classmethod
    def _generate_variants_fnc(cls, resource, name):
        variants = copy.copy(resource.properties)
        variants[resource.VariantKey] = resource.name
        variants[cls.VariantKey] = name
        return variants

    def __init__(self, resource, name):
        super(_ResourceTask, self).__init__(
            resource.stage, self._generate_variants_fnc(resource, name)
        )

        self._resource = resource
        self._project = resource.project

    def __new__(cls, resource, name):
        stage = resource.stage
        path = cls._generate_path_fnc(resource, name)
        if path in stage.ENTITY_INSTANCE_DICT:
            return stage.ENTITY_INSTANCE_DICT[path]
        instance = super(_ResourceTask, cls).__new__(cls, resource, name)
        stage.ENTITY_INSTANCE_DICT[path] = instance
        if cls.VERBOSE_LEVEL < 1:
            sys.stdout.write('new {}: {}\n'.format(cls.VariantKey, path))
        return instance

    @property
    def project(self):
        return self._project

    @property
    def resource(self):
        return self._resource


class AssetTask(_ResourceTask):
    ENTITY_PATH_PTN = '/{project}/{asset}/{task}'

    def __init__(self, asset, name):
        super(AssetTask, self).__init__(asset, name)


class SequenceTask(_ResourceTask):
    ENTITY_PATH_PTN = '/{project}/{sequence}/{task}'

    def __init__(self, asset, name):
        super(SequenceTask, self).__init__(asset, name)


class ShotTask(_ResourceTask):
    ENTITY_PATH_PTN = '/{project}/{shot}/{task}'

    def __init__(self, asset, name):
        super(ShotTask, self).__init__(asset, name)
