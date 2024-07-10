# coding:utf-8
import collections

import sys

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import qsm_maya.core as qsm_mya_core


class Util(object):
    class DataKeys:
        Node = 'node'
        Transform = 'transform'
        Sources = 'sources'
        Targets = 'targets'

    class ExportScheme:
        Node = 'node'
        NodeGraph = 'node_graph'

    def __init__(self, path):
        self._node_path = path
        self._dcc_node_opt_list = qsm_mya_core.BscNodeOpt(path)

    @classmethod
    def get_node_properties(cls, path, includes=None):
        if path is None:
            raise RuntimeError()

        if qsm_mya_core.Node.is_exists(path) is False:
            raise RuntimeError()

        node_opt = qsm_mya_core.BscNodeOpt(path)
        if isinstance(includes, (tuple, list)):
            _ = includes
        else:
            _ = node_opt.get_all_port_paths()
        return node_opt.get_node_properties(includes=_)

    @classmethod
    def apply_node_properties(cls, path, data, *args, **kwargs):
        if path is None:
            raise RuntimeError()

        if qsm_mya_core.Node.is_exists(path) is False:
            raise RuntimeError()

        node_opt = qsm_mya_core.BscNodeOpt(path)
        node_opt.apply_node_properties(
            data, *args, **kwargs
        )


class AbsNodeOpt(object):

    SCHEME_BASE = '/node/any'

    TYPE_INCLUDES = []

    SCR_TYPE_PATH_MAPPER = dict(
        # deform
        deformBend='/nodes/non_linear/bend',
        deformFlare='/nodes/non_linear/flare',
        deformSine='/nodes/non_linear/sine',
        deformSquash='/nodes/non_linear/squash',
        deformTwist='/nodes/non_linear/twist',
        deformWave='/nodes/non_linear/wave',
        # xform
        nucleus='/nodes/nucleus/nucleus',
        #
        airField='/nodes/fields/air_field',
        dragField='/nodes/fields/drag_field',
        gravityField='/nodes/fields/gravity_field',
        newtonField='/nodes/fields/newton_field',
        radialField='/nodes/fields/radial_field',
        turbulenceField='/nodes/fields/turbulence_field',
        uniformField='/nodes/fields/uniform_field',
        vortexField='/nodes/fields/vortex_field',
        # nucleus
        hairSystem='/nodes/nucleus/n_hair',
        nCloth='/nodes/nucleus/n_cloth',
        nRigid='/nodes/nucleus/n_rigid',
        nParticle='/nodes/nucleus/n_particle',
        # motion
        motionPath='/nodes/constrains/motion_path',
    )

    DATA_KEY_INCLUDES = [
        Util.DataKeys.Node
    ]

    TARGET_ARGS = [
    ]

    SOURCE_ARGS = [
    ]

    def __init__(self, node_path):
        self._node_path = node_path
        self._node_type = qsm_mya_core.Node.get_type(self._node_path)

        self._get_fnc_mapper = {
            Util.DataKeys.Node: self.get_for_node,
            Util.DataKeys.Transform: self.get_for_transform,
            Util.DataKeys.Sources: self.get_for_sources,
            Util.DataKeys.Targets: self.get_for_targets
        }
        self._apply_fnc_mapper = {
            Util.DataKeys.Node: self.apply_for_node,
            Util.DataKeys.Transform: self.apply_for_transform,
            Util.DataKeys.Sources: self.apply_for_sources,
            Util.DataKeys.Targets: self.apply_for_targets
        }

        sys.stdout.write('current is "{}:{}", scheme is "{}"\n'.format(
            self._node_type, self._node_path,
            self.get_scheme())
        )

    def get_scheme(self):
        return '{}/{}'.format(self.SCHEME_BASE, self._node_type)

    def get_for_transform(self):
        _ = qsm_mya_core.Shape.get_transform(self._node_path)
        if _:
            path = _
            return Util.get_node_properties(path)

    def apply_for_transform(self, data, *args, **kwargs):
        _ = qsm_mya_core.Shape.get_transform(self._node_path)
        if _:
            path = _
            return Util.apply_node_properties(path, data, *args, **kwargs)

    def get_for_sources(self):
        dict_ = {}
        for i in self.SOURCE_ARGS:
            i_atr_name, i_node_type = i
            i_key = '{}:{}'.format(*i)
            _ = qsm_mya_core.NodeAttribute.get_source_node(
                self._node_path, i_atr_name, i_node_type
            )
            if _:
                i_path = _
                dict_[i_key] = Util.get_node_properties(i_path)
        return dict_

    def apply_for_sources(self, data, *args, **kwargs):
        for i_k, i_data in data.items():
            i_atr_name, i_node_type = i_k.split(':')
            _ = qsm_mya_core.NodeAttribute.get_source_node(
                self._node_path, i_atr_name, i_node_type
            )
            if _:
                i_path = _
                Util.apply_node_properties(i_path, i_data, *args, **kwargs)

    def get_for_targets(self):
        dict_ = {}
        for i in self.TARGET_ARGS:
            i_atr_name, i_node_type = i
            i_key = '{}:{}'.format(*i)
            _ = qsm_mya_core.NodeAttribute.get_target_nodes(
                self._node_path, i_atr_name, i_node_type
            )
            if _:
                i_path = _[0]
                dict_[i_key] = Util.get_node_properties(i_path)
        return dict_

    def apply_for_targets(self, data, *args, **kwargs):
        for i_k, i_data in data.items():
            i_atr_name, i_node_type = i_k.split(':')
            _ = qsm_mya_core.NodeAttribute.get_target_nodes(
                self._node_path, i_atr_name, i_node_type
            )
            if _:
                i_path = _[0]
                Util.apply_node_properties(i_path, i_data, *args, **kwargs)

    def to_scr_type_path(self):
        if self._node_type in self.SCR_TYPE_PATH_MAPPER:
            return self.SCR_TYPE_PATH_MAPPER[self._node_type]
        return '/nodes/other'

    def get_for_node(self):
        path = self._node_path
        return Util.get_node_properties(path)

    def apply_for_node(self, data, *args, **kwargs):
        Util.apply_node_properties(self._node_path, data, *args, **kwargs)

    def get_data(self):
        data = collections.OrderedDict()
        for i_key in self.DATA_KEY_INCLUDES:
            i_fnc = self._get_fnc_mapper[i_key]
            i_data = i_fnc()
            if i_data:
                data[i_key] = i_fnc()
        return dict(
            scheme=self.get_scheme(),
            data=data
        )

    @qsm_mya_core.Undo.execute
    def apply_data(self, file_path, frame_offset=0, force=True, excludes=None, key_includes=None):
        node_data = bsc_storage.StgFileOpt(file_path).set_read()
        scheme = node_data.get('scheme')
        if scheme == self.get_scheme():
            data = node_data.get('data')
            if isinstance(key_includes, (tuple, list)):
                keys = key_includes
            else:
                keys = self.DATA_KEY_INCLUDES
            for i_key in keys:
                if i_key in data:
                    i_data = data[i_key]
                    i_fnc = self._apply_fnc_mapper[i_key]
                    i_fnc(i_data, frame_offset=frame_offset, force=force, excludes=excludes)

    @classmethod
    def check_is_valid(cls, node_type):
        if cls.TYPE_INCLUDES:
            if node_type in cls.TYPE_INCLUDES:
                return True
            return False
        return True
    

class AbsNodeCreator(object):
    def __init__(self, target_node_path, target_any_paths, scheme):
        self._target_node_path = target_node_path
        self._target_any_paths = target_any_paths
        self._scheme = scheme
        self._node_type = self._scheme.split('/')[-1]

    @qsm_mya_core.Undo.execute
    def do_create(self):
        pass


class AbsShapeOpt(AbsNodeOpt):
    SCHEME_BASE = '/node/shape'

    DATA_KEY_INCLUDES = [
        Util.DataKeys.Node,
        Util.DataKeys.Transform
    ]

    def __init__(self, *args, **kwargs):
        super(AbsShapeOpt, self).__init__(*args, **kwargs)

    def find_transform(self):
        return qsm_mya_core.Shape.get_transform(self._node_path)


class AbsNodeGraphOpt(object):
    SCHEME_BASE = '/node_graph'

    TYPE_INCLUDES = []

    def __init__(self, node_paths):
        self._node_paths = node_paths
        self._node_type = qsm_mya_core.Node.get_type(self._node_paths)

        sys.stdout.write(
            'scheme is "{}"\n'.format(
                self.get_scheme()
            )
        )

    def get_scheme(self):
        return self.SCHEME_BASE
    
    def get_data(self):
        directory_path_tmp = '{}/{}'.format(
            bsc_storage.StgUser.get_user_temporary_directory(),
            bsc_core.BscUuid.generate_new()
        )
        file_path = '{}/node-graph.ma'.format(directory_path_tmp)
        qsm_mya_core.SceneFile.export_as_node_graph(
            file_path, self._node_paths
        )
        return file_path
    
    def apply_data(self, file_path, frame_offset=None):
        print frame_offset
        nodes = qsm_mya_core.SceneFile.import_as_node_graph(
            file_path
        )
        if frame_offset is not None:
            for i in nodes:
                if qsm_mya_core.AnmCurve.check_is_valid(i):
                    qsm_mya_core.AnmCurve.offset_frame(i, frame_offset)
    
    @classmethod
    def check_is_valid(cls, node_type):
        if cls.TYPE_INCLUDES:
            if node_type in cls.TYPE_INCLUDES:
                return True
            return False
        return True
