# coding:utf-8
import collections
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core

from . import base as _base


class GpuInstanceOpt(object):
    IMPORT_ROOT = '|__GPU_INSTANCE_IMPORT__'

    @classmethod
    def create_import_root(cls):
        return qsm_mya_core.Group.create(
            cls.IMPORT_ROOT
        )

    @classmethod
    def create_import_location(cls, namespace):
        root = cls.create_import_root()
        location = '{}|{}_MESH_GRP'.format(root, namespace)
        return qsm_mya_core.Group.create(
            location
        )

    def __init__(self, node):
        self._node = node
        self._shape = qsm_mya_core.Transform.get_shape(self._node)

        self._path = None
        self._path_opt = None

    def __str__(self):
        return '{}(path="{}")'.format(
            self.__class__.__name__, self._path or self._node
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._node == other._node
        return False

    def is_exists(self):
        return qsm_mya_core.Node.is_exists(self._node)

    @property
    def path(self):
        return self._path

    @property
    def path_opt(self):
        return self._path_opt

    @property
    def node(self):
        return self._node

    def get_active(self):
        file_path = qsm_mya_core.NodeAttribute.get_as_string(
            self._shape, 'cacheFileName'
        )
        if file_path:
            return bsc_storage.StgFileOpt(file_path).name_base

    def set_active(self, key):
        file_path = qsm_mya_core.NodeAttribute.get_as_string(
            self._shape, 'cacheFileName'
        )
        file_opt = bsc_storage.StgFileOpt(file_path)
        if file_opt.get_is_file() is True:
            file_path_new = '{}/{}.abc'.format(
                file_opt.directory_path, key
            )
            if bsc_storage.StgPath.get_is_file(file_path_new) is True:
                qsm_mya_core.NodeAttribute.set_as_string(
                    self._shape, 'cacheFileName', file_path_new
                )

    def do_import_mesh(self):
        file_path = qsm_mya_core.NodeAttribute.get_as_string(
            self._shape, 'cacheFileName'
        )
        file_opt = bsc_storage.StgFileOpt(file_path)
        if file_opt.get_is_file() is True:
            mesh_file_path = '{}/mesh.mb'.format(file_opt.directory_path)

            namespace = qsm_mya_core.DagNode.extract_namespace(self._node)

            import_location = self.create_import_location(namespace)

            paths = qsm_mya_core.SceneFile.import_file(mesh_file_path, namespace)
            roots = qsm_mya_core.DagNode.find_roots(paths)
            for i in roots:
                i_path_new = qsm_mya_core.DagNode.parent_to(
                    i, import_location
                )

                qsm_mya_core.Node.delete(
                    qsm_mya_core.ParentConstraint.create(
                        self._node, i_path_new
                    )
                )
                qsm_mya_core.Node.delete(
                    qsm_mya_core.ScaleConstraint.create(
                        self._node, i_path_new
                    )
                )

            qsm_mya_core.NodeAttribute.set_visible(
                self._node, False
            )

    def set_lod(self, lod):
        if lod == 0:
            self.set_active(_base.Assembly.Keys.GPU)
        else:
            self.set_active(_base.Assembly.Keys.GPU_LOD.format(lod))


class GpuInstancesQuery(object):
    def __init__(self):
        self._cache_hash_key = None
        self._cache_dict = collections.OrderedDict()
        self._path_query = dict()

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
        self._path_query.clear()
        for i_k, i_v in data.items():
            for j_seq, j_path in enumerate(i_v):
                j_name = j_path.split('|')[-1]
                j_path_virtual = '/{}/{}_{}'.format(i_k, j_name, j_seq)
                j_opt = GpuInstanceOpt(j_path)
                j_opt._path = j_path_virtual
                j_opt._path_opt = bsc_core.BscNodePathOpt(j_path_virtual)
                self._cache_dict[j_path_virtual] = j_opt

                self._path_query[j_path] = j_opt

    def get_all(self):
        return list(self._cache_dict.values())

    def to_mapper(self, paths):
        dict_ = {}
        for i_path in paths:
            i_result = self.find_one(i_path)
            if i_result is not None:
                i_active = GpuInstanceOpt(i_result).get_active()
                dict_.setdefault(
                    i_active, set()
                ).add(i_result)
        return dict_

    @classmethod
    def find_one(cls, path):
        if qsm_mya_core.Node.is_transform_type(path):
            _ = path
        elif qsm_mya_core.Node.is_gpu(path):
            _ = qsm_mya_core.Shape.get_transform(path)
        else:
            return None

        if qsm_mya_core.NodeAttribute.get_is_value(
            _, 'qsm_type', _base.Assembly.Types.GpuInstance
        ) is True:
            return _

    @classmethod
    def get_data(cls):
        dict_ = {}
        _ = cmds.ls(type='transform', long=1)
        for i_path in _:
            if cmds.objExists(i_path+'.qsm_type') is True:
                i_qsm_type = qsm_mya_core.NodeAttribute.get_as_string(i_path, 'qsm_type')
                if i_qsm_type == 'gpu_instance':
                    i_qsm_hash_key = qsm_mya_core.NodeAttribute.get_as_string(i_path, 'qsm_hash_key')
                    dict_.setdefault(
                        i_qsm_hash_key, []
                    ).append(i_path)
        return dict_
