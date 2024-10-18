# coding:utf-8
import collections

import copy
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.log as bsc_log

from ... import core as _mya_core


class Asset(object):
    def __init__(self, namespace):
        self._namespace = namespace
        self._node = None
        self._file_path = None
        self._path = None
        self._path_opt = None
        self._variants = None

    def __str__(self):
        return '{}(path="{}")'.format(
            self.__class__.__name__, self._path
        )

    def __repr__(self):
        return self.__str__()

    @property
    def reference(self):
        return self._node

    @property
    def reference_opt(self):
        return _mya_core.ReferenceOpt(self._node)

    @property
    def file(self):
        return self._file_path

    @property
    def namespace(self):
        return self._namespace

    @property
    def path(self):
        return self._path

    @property
    def path_opt(self):
        return self._path_opt

    @property
    def variants(self):
        return self._variants

    def is_exists(self):
        return _mya_core.Namespace.is_exists(self._namespace)

    def find_nodes_by_scheme(self, scheme):
        raise NotImplementedError()

    def get_all_for_isolate_select(self):
        roots = cmds.ls('|{}:*'.format(self._namespace), long=1) or []
        return roots


class AssetsQuery(object):
    LOG_KEY = 'resource query'

    STG_PTN = 'X:/{project}/Assets/{role}/{asset}/Maya/Final/{asset}.ma'

    DAG_PTN = '/{namespace}'

    RESOURCE_CLS = Asset

    def __init__(self):
        self._pth = bsc_core.BscStgParseOpt(
            self.STG_PTN
        )
        self._cache_hash_key = None
        self._cache_dict = collections.OrderedDict()

        # self.do_update()

    def __str__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            self._cache_dict.values()
        )

    def __repr__(self):
        return '\n'+self.__str__()

    def check_is_valid(self, *args, **kwargs):
        file_path = kwargs['file']
        return self._pth.check_is_matched(file_path)

    def do_update(self):
        data = self.get_data()
        hash_key = bsc_core.BscHash.to_hash_key(data)
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
        self._cache_dict.clear()
        keys = data.keys()
        keys.sort()
        for i_namespace in keys:
            i_node_path, i_is_loaded, i_file_path, i_variants = data[i_namespace]
            i_resource = self.RESOURCE_CLS(i_namespace)
            i_resource._node = i_node_path
            i_resource._file_path = i_file_path
            i_kwargs = copy.copy(i_variants)
            i_kwargs['namespace'] = i_namespace
            i_path_virtual = self.DAG_PTN.format(**i_kwargs)
            i_resource._path = i_path_virtual
            i_resource._path_opt = bsc_core.BscPathOpt(i_path_virtual)
            i_resource._variants = i_variants
            self._cache_dict[i_namespace] = i_resource

    def get_data(self):
        dict_ = {}
        _ = _mya_core.References.get_all(nested=True)
        for i_path in _:
            i_args = _mya_core.Reference.get_args(i_path)
            if i_args is None:
                bsc_log.Log.trace_warning(
                    'invalid reference: "{}"'.format(i_path)
                )
                continue

            i_namespace, i_file_path, i_is_loaded = i_args
            # check file path
            if self.check_is_valid(namespace=i_namespace, file=i_file_path, is_loaded=i_is_loaded) is True:
                i_variants = self._pth.get_variants(i_file_path)
                dict_[i_namespace] = i_path, i_is_loaded, i_file_path, i_variants
        return dict_

    def get_all(self):
        return self._cache_dict.values()

    def get(self, namespace):
        if namespace in self._cache_dict:
            return self._cache_dict[namespace]

    def to_valid_namespaces(self, namespaces):
        return [i for i in namespaces if i in self._cache_dict]


class AssetCacheOpt(object):
    CACHE_ROOT = None
    CACHE_NAME = None

    def __init__(self, resource):
        self._resource = resource
        self._namespace = resource.namespace
        self._file_path = resource.file

    def is_exists(self):
        _ = cmds.ls('{}:{}'.format(self._namespace, self.CACHE_NAME), long=1)
        return not not _

    def is_resource_exists(self):
        return self._resource.is_exists()

    def remove_cache(self):
        _ = cmds.ls('{}:{}'.format(self._namespace, self.CACHE_NAME), long=1)
        if _:
            cmds.delete(_[0])

    @classmethod
    def create_cache_root_auto(cls):
        if cmds.objExists(cls.CACHE_ROOT) is False:
            name = cls.CACHE_ROOT.split('|')[-1]
            # cmds.container(type='dagContainer', name=name)
            cmds.createNode(
                'dagContainer', name=name, shared=1, skipSelect=1
            )
            cmds.setAttr(cls.CACHE_ROOT+'.iconName', 'folder-closed.png', type='string')

    def load_cache(self, *args, **kwargs):
        raise NotImplementedError()

    def remove_resource_auto(self, *args, **kwargs):
        raise NotImplementedError()

    def generate_args(self, *args, **kwargs):
        raise NotImplementedError()
