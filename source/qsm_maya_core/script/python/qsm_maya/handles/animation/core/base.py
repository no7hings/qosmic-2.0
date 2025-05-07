# coding:utf-8
from __future__ import print_function
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.content as bsc_content

import lxbasic.resource as bsc_resource

import qsm_general.core as qsm_gnl_core


class AdvQuery(object):

    def __init__(self, namespace):
        ctt = bsc_resource.BscConfigure.get_as_content(
            'maya/rig/adv'
        )
        ctt.set('option.namespace', namespace)
        ctt.do_flatten()

        self._main_ctt = bsc_content.Dict(value=ctt.get('main'))
        self._main_query = bsc_content.Dict()

        if qsm_gnl_core.scheme_is_release():
            self._skeleton_ctt = bsc_content.Dict(value=ctt.get('skeleton_new'))
        else:
            self._skeleton_ctt = bsc_content.Dict(value=ctt.get('skeleton'))
        self._skeleton_query = bsc_content.Dict()

        self._rotation_ctt = bsc_content.Dict(value=ctt.get('rotation'))
        self._rotation_query = bsc_content.Dict()

        self._distance_query = bsc_content.Dict(value=ctt.get('distance'))
        if qsm_gnl_core.scheme_is_release():
            self._geometry_query = bsc_content.Dict(value=ctt.get('geometry_new'))
        else:
            self._geometry_query = bsc_content.Dict(value=ctt.get('geometry'))

        self.do_update()

    def do_update(self):
        keys = self._main_ctt.get_all_leaf_keys()
        for i_key in keys:
            i_value = self._main_ctt.get(i_key)
            i_results = cmds.ls(i_value, long=1)
            self._main_query.set(i_key, i_results)

        keys = self._skeleton_ctt.get_all_leaf_keys()
        for i_key in keys:
            i_value = self._skeleton_ctt.get(i_key)
            i_results = cmds.ls(i_value, long=1)
            self._skeleton_query.set(i_key, i_results)

        keys = self._rotation_ctt.get_all_leaf_keys()
        for i_key in keys:
            i_value = self._rotation_ctt.get(i_key)
            self._rotation_query.set(i_key, i_value)

    @property
    def main_query(self):
        return self._main_query

    @property
    def skeleton_query(self):
        return self._skeleton_query

    @property
    def rotation_query(self):
        return self._rotation_query

    @property
    def distance_query(self):
        return self._distance_query

    @property
    def geometry_query(self):
        return self._geometry_query

    def test(self):
        print(self._skeleton_query)
