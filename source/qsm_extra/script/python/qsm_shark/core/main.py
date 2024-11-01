# coding:utf-8
import lxbasic.resource as bsc_resource

import lxbasic.core as bsc_core

import _abc

import _root


class Stage(_abc.AbsBase):
    INSTANCE_DICT = dict()

    ENTITY_INSTANCE_DICT = dict()

    def generate_location_for(self, key, variants):
        return self._main_configure.get(key).format(**variants)

    def __init__(self, scheme='TEST'):
        self._scheme = scheme
        self._main_configure = bsc_resource.RscExtendConfigure.get_as_content('shark/{}'.format(self._scheme))
        self._main_configure.do_flatten()
        self._platform = bsc_core.BscPlatform.get_current()
        self._root_location = self._main_configure.get('root-dir.{}'.format(self._platform))
        self._root = _root.Root(self, self._root_location)
        self._properties = dict()

    def __new__(cls, *args, **kwargs):
        scheme = kwargs.get('scheme', 'TEST')
        if scheme in cls.INSTANCE_DICT:
            return cls.INSTANCE_DICT[scheme]

        instance = super(Stage, cls).__new__(cls, *args, **kwargs)
        cls.INSTANCE_DICT[scheme] = instance
        return instance

    @property
    def platform(self):
        return self._platform

    @property
    def root(self):
        return self._root

    @property
    def properties(self):
        return self._properties

    # project
    def find_project(self, name):
        return self._root.find_project(name)

    # asset
    def find_asset(self, project, asset):
        return self.find_project(project).find_asset(asset)

    def find_asset_task(self, project, asset, task):
        return self.find_project(project).find_asset(asset).find_task(task)

    # sequence
    def find_sequence(self, project, sequence):
        return self.find_project(project).find_sequence(sequence)

    def find_sequence_task(self, project, asset, task):
        return self.find_project(project).find_sequence(asset).find_task(task)

    # shot
    def find_shot(self, project, shot):
        return self.find_project(project).find_shot(shot)

    def find_shot_task(self, project, asset, task):
        return self.find_project(project).find_shot(asset).find_task(task)
