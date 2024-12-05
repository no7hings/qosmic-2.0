# coding:utf-8
import sys

import copy

import _abc


class Role(_abc.AbsEntity):
    @classmethod
    def _generate_variants_fnc(cls, project, name):
        variants = copy.copy(project.properties)
        variants[cls.VariantKey] = name
        return variants

    def __init__(self, project, name):
        super(Role, self).__init__(
            project.stage, self._generate_variants_fnc(project, name)
        )

        self._project = project
