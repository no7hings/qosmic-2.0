# coding:utf-8
import collections

import copy
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

from ... import core as _mya_core


class ResourceOpt(object):
    def __init__(self, namespace):
        self.namespace = namespace
        self.reference = None

    @property
    def reference_opt(self):
        return _mya_core.ReferenceOpt(self.reference)

    def __str__(self):
        return '{}(path="{}")'.format(
            self.__class__.__name__,
            self.__dict__['path']
        )
    
    def find_nodes_by_scheme(self, scheme):
        raise NotImplementedError()


class ResourcesQuery(object):
    STG_PTN = 'X:/{project}/Assets/{role}/{asset}/Maya/Final/{asset}.ma'

    DAG_PTN = '/{namespace}'

    RESOURCE_CLS = ResourceOpt

    def __init__(self):
        self._pth = bsc_core.PtnStgParseOpt(
            self.STG_PTN
        )
        self._cache_hash_key = None
        self._cache_dict = collections.OrderedDict()

        # self.do_update()

    def do_update(self):
        data = self.get_reference_data()
        hash_key = bsc_core.HashMtd.to_hash_key(data)
        if self._cache_hash_key is None:
            self.do_update_by(data)
            self._cache_hash_key = hash_key
            return True
        else:
            if self._cache_hash_key != hash_key:
                self.do_update_by(data)
                self._cache_hash_key = hash_key
                return True
        return False

    def do_update_by(self, data):
        self._cache_dict = collections.OrderedDict()
        for i_namespace, (i_reference, i_file_path, i_variants) in data.items():
            i_resource_opt = self.RESOURCE_CLS(i_namespace)
            i_resource_opt.reference = i_reference
            i_kwargs = copy.copy(i_variants)
            i_kwargs['namespace'] = i_namespace
            i_path_virtual = self.DAG_PTN.format(**i_kwargs)
            i_resource_opt.path = i_path_virtual
            i_resource_opt.path_opt = bsc_core.PthNodeOpt(i_path_virtual)
            i_resource_opt.variants = i_variants
            self._cache_dict[i_namespace] = i_resource_opt

    def get_reference_data(self):
        dict_ = {}
        _ = _mya_core.References.get_all()
        for i_path in _:
            i_file_path = _mya_core.Reference.get_file(i_path)
            if self._pth.get_is_matched(i_file_path) is True:
                i_namespace = cmds.referenceQuery(i_path, namespace=1, shortName=1)
                i_variants = self._pth.get_variants(i_file_path)
                dict_[i_namespace] = i_path, i_file_path, i_variants
        return dict_

    def get_all(self):
        return self._cache_dict.values()

    def to_valid_namespaces(self, namespaces):
        return [i for i in namespaces if i in self._cache_dict]
