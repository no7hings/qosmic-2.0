# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxcontent.core as ctt_core

import lxresource as bsc_resource

SCHEME = 'default'


class AdvQuery(object):

    def __init__(self, namespace):
        ctt = bsc_resource.RscExtendConfigure.get_as_content(
            'rig/adv'
        )
        ctt.set('option.namespace', namespace)
        ctt.do_flatten()

        self._main_ctt = ctt_core.Dict(value=ctt.get('main'))
        self._main_query = ctt_core.Dict()

        if SCHEME == 'new':
            self._skeleton_ctt = ctt_core.Dict(value=ctt.get('skeleton_new'))
        else:
            self._skeleton_ctt = ctt_core.Dict(value=ctt.get('skeleton'))
        self._skeleton_query = ctt_core.Dict()

        self._rotation_ctt = ctt_core.Dict(value=ctt.get('rotation'))
        self._rotation_query = ctt_core.Dict()

        self._distance_query = ctt_core.Dict(value=ctt.get('distance'))
        if SCHEME == 'new':
            self._geometry_query = ctt_core.Dict(value=ctt.get('geometry_new'))
        else:
            self._geometry_query = ctt_core.Dict(value=ctt.get('geometry'))

        self._cache_all()

    def _cache_all(self):
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
        print self._skeleton_query

