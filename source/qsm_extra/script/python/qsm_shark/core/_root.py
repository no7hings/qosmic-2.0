# coding:utf-8
import _base

import _abc

import _project


class Root(_abc.AbsEntity):
    EntityType = _base.EntityTypes.Root
    VariantKey = _base.VariantKeys.Root

    ENTITY_PATH_PTN = '/'

    def __init__(self, stage, location):
        super(Root, self).__init__(
            stage,
            variants=dict(root=location)
        )

        self._location = location

    def get_location(self):
        return self._location

    def find_project(self, name):
        return _project.Project(
            self, name
        )
