# coding:utf-8
import sys

import copy

import _base

import _abc

import _resource


class Project(_abc.AbsEntity):
    EntityType = _base.EntityTypes.Project
    VariantKey = _base.VariantKeys.Project

    ENTITY_PATH_PTN = '/{project}'

    @classmethod
    def _generate_variants_fnc(cls, root, name):
        variants = copy.copy(
            root.properties
        )
        variants[cls.VariantKey] = name
        return variants

    def __init__(self, root, name):
        super(Project, self).__init__(
            root.stage,
            self._generate_variants_fnc(root, name)
        )

    def __new__(cls, root, name):
        stage = root.stage
        path = cls._generate_path_fnc(root, name)
        if path in stage.ENTITY_INSTANCE_DICT:
            return stage.ENTITY_INSTANCE_DICT[path]
        instance = super(Project, cls).__new__(cls, stage, name)
        stage.ENTITY_INSTANCE_DICT[path] = instance
        if cls.VERBOSE_LEVEL < 1:
            sys.stdout.write('new {}: {}\n'.format(cls.VariantKey, path))
        return instance

    def find_asset(self, name):
        return _resource.Asset(
            self, name
        )

    def find_sequence(self, name):
        return _resource.Sequence(
            self, name
        )

    def find_shot(self, name):
        return _resource.Shot(
            self, name
        )
