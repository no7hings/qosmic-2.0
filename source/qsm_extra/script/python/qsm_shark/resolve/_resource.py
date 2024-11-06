# coding:utf-8
import sys

import copy

import _base

import _abc

import _task


class _Resource(_abc.AbsEntity):
    ENTITY_TASK_CLS = None

    @classmethod
    def _generate_variants_fnc(cls, project, name):
        variants = copy.copy(
            project.properties
        )
        variants[cls.VariantKey] = name
        return variants

    def __init__(self, project, name):
        super(_Resource, self).__init__(
            project.stage, self._generate_variants_fnc(project, name)
        )

        self._project = project

    def __new__(cls, project, name):
        stage = project.stage
        path = cls._generate_path_fnc(project, name)
        if path in stage.ENTITY_INSTANCE_DICT:
            return stage.ENTITY_INSTANCE_DICT[path]
        instance = super(_Resource, cls).__new__(cls, project, name)
        stage.ENTITY_INSTANCE_DICT[path] = instance
        if cls.VERBOSE_LEVEL < 1:
            sys.stdout.write('new {}: {}\n'.format(cls.VariantKey, path))
        return instance

    @property
    def project(self):
        return self._project

    def find_task(self, name):
        return self.ENTITY_TASK_CLS(
            self, name
        )


class Asset(_Resource):
    EntityType = _base.EntityTypes.Asset
    VariantKey = _base.VariantKeys.Asset

    ENTITY_PATH_PTN = '/{project}/{asset}'

    ENTITY_TASK_CLS = _task.AssetTask

    def __init__(self, project, name):
        super(Asset, self).__init__(project, name)


class Sequence(_Resource):
    EntityType = _base.EntityTypes.Sequence
    VariantKey = _base.VariantKeys.Sequence

    ENTITY_PATH_PTN = '/{project}/{sequence}'

    ENTITY_TASK_CLS = _task.SequenceTask

    def __init__(self, project, name):
        super(Sequence, self).__init__(project, name)


class Shot(_Resource):
    EntityType = _base.EntityTypes.Shot
    VariantKey = _base.VariantKeys.Shot

    ENTITY_PATH_PTN = '/{project}/{shot}'

    ENTITY_TASK_CLS = _task.ShotTask

    def __init__(self, project, name):
        super(Shot, self).__init__(project, name)
