# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.resource as bsc_resource

import qsm_maya.core as qsm_mya_core

from .. import core as _core


class _FilterCache(object):
    def __init__(self):
        self._cache_dict = {}
    
    def generate(self, shape_paths):
        nodes = set()
        for i_shape_path in shape_paths:
            if i_shape_path in self._cache_dict:
                nodes.add(self._cache_dict[i_shape_path])
            else:
                i_path_new = self.filter_fnc(i_shape_path)
                self._cache_dict[i_shape_path] = i_path_new
                nodes.add(i_path_new)
        return list(nodes)
    
    @classmethod
    def filter_fnc(cls, shape_path):
        if cmds.nodeType(shape_path) == 'mesh':
            assembly_path = _core.Assembly.find_assembly_reference(shape_path)
            if assembly_path is not None:
                return assembly_path
            return shape_path
        return shape_path


class CameraViewFrustum(object):
    CONTAINER_NAME = 'camera_view_frustum_dgc'

    CAMERA_FRUSTUM = '|__CAMERA_FRUSTUM__'

    def __init__(self, camera=None):
        if camera is None:
            self._camera_path = qsm_mya_core.Camera.get_active()
        else:
            self._camera_path = qsm_mya_core.DagNode.to_path(camera)

        if not self._camera_path:
            raise RuntimeError()

    @classmethod
    def restore(cls):
        path = '|{}'.format(cls.CONTAINER_NAME)
        if qsm_mya_core.DagNode.is_exists(path):
            qsm_mya_core.DagNode.delete(path)

    def create_container(self):
        path = '|{}'.format(self.CONTAINER_NAME)
        qsm_mya_core.Container.create_as_expression(
            path
        )
        cmds.setAttr(path+'.blackBox', 1, lock=1)
        cmds.setAttr(path+'.hiddenInOutliner', 1)
        return path

    @qsm_mya_core.Undo.execute
    def execute(self):
        self.restore()

        container = self.create_container()

        qsm_mya_core.SceneFile.import_file_ignore_error(
            bsc_resource.BscResource.get('rig/camera_frustum.ma')
        )
        transform_path = qsm_mya_core.Shape.get_transform(self._camera_path)
        name = self._camera_path.split('|')[-1]
        frustum_name = '{}_fst'.format(name)
        eps_name = '{}_eps'.format(name)
        frustum_transform_path = qsm_mya_core.DagNode.rename(
            self.CAMERA_FRUSTUM, frustum_name
        )
        eps_script = (
            '$f = {camera}.focalLength;\n'
            '$fbw = {camera}.horizontalFilmAperture*25.4;\n'
            '$w = defaultResolution.width;\n'
            '$h = defaultResolution.height;\n'
            '{box}.scaleZ = {camera}.farClipPlane*1.0;\n'
            '{box}.scaleX = $fbw/$f*{box}.scaleZ;\n'
            '{box}.scaleY = $fbw/$f*{box}.scaleZ*(($h*1.0)/($w*1.0));'
        ).format(
            camera=self._camera_path, box=frustum_transform_path
        )
        qsm_mya_core.ParentConstraint.create(transform_path, frustum_transform_path)
        qsm_mya_core.Expression.create(
            eps_name, eps_script, frustum_transform_path
        )
        qsm_mya_core.Container.add_dag_nodes(container, [frustum_transform_path], relative=True)
        qsm_mya_core.Container.add_nodes(container, [eps_name])


class DynamicCameraMask(object):
    CONTAINER_NAME = 'dynamic_camera_mask_dgc'

    def __init__(self, camera=None, frame=None):
        cmds.loadPlugin('gpuCache', quiet=1)

        if camera is None:
            self._camera_path = qsm_mya_core.Camera.get_active()
        else:
            self._camera_path = qsm_mya_core.DagNode.to_path(camera)

        if not self._camera_path:
            raise RuntimeError()

        self._frame = frame
        self._frame_range = qsm_mya_core.Frame.auto_range(self._frame)

        self._node_dict = {}
        self._filter_cache = _FilterCache()

    @classmethod
    def restore(cls):
        atr_paths = []
        path = '|{}'.format(cls.CONTAINER_NAME)
        if qsm_mya_core.DagNode.is_exists(path):
            nodes = qsm_mya_core.Container.find_all_nodes(path, type_includes=['plusMinusAverage'])
            for i in nodes:
                i_targets = qsm_mya_core.NodeAttribute.get_targets(i, 'output1D')
                if i_targets:
                    atr_paths.extend(i_targets)
            qsm_mya_core.DagNode.delete(path)

        for i in atr_paths:
            cmds.setAttr(i, 1)

    def create_container(self):
        path = '|{}'.format(self.CONTAINER_NAME)
        qsm_mya_core.Container.create_as_expression(
            path
        )
        qsm_mya_core.NodeAttribute.create_as_integer(
            path, 'qsm_start_fame', self._frame_range[0]
        )
        qsm_mya_core.NodeAttribute.create_as_integer(
            path, 'qsm_end_fame', self._frame_range[1]
        )
        cmds.setAttr(path+'.hiddenInOutliner', 1)
        cmds.setAttr(path+'.blackBox', 1, lock=1)
        return path

    def generate_mask_nodes_at_frame(self, frame):
        qsm_mya_core.Frame.set_current(frame)

        results = qsm_mya_core.Camera.generate_mask_nodes(
            self._camera_path, type_includes=['mesh', 'gpuCache']
        )

        list_ = []
        for i_path in results:
            if qsm_mya_core.DagNode.is_mesh_type(i_path):
                if qsm_mya_core.Mesh.is_deformed(i_path) is False:
                    list_.append(i_path)
            else:
                list_.append(i_path)
        return list_

    def nodes_pre_prc(self, all_paths):
        nodes = []
        for i_index, i_shape_path in enumerate(all_paths):
            # ignore deformed mesh
            if qsm_mya_core.DagNode.is_mesh_type(i_shape_path) is True:
                if qsm_mya_core.Mesh.is_deformed(i_shape_path) is True:
                    continue

            i_sum_name = 'camera_mask_{}_sum'.format(i_index)
            qsm_mya_core.Node.create(
                i_sum_name, 'plusMinusAverage'
            )
            self._node_dict[i_shape_path] = i_sum_name

            nodes.append(i_sum_name)
        return nodes

    def nodes_post_prc(self, container):
        for i_any_path, v in self._node_dict.items():
            if qsm_mya_core.Reference.is_from_reference(i_any_path) is True:
                qsm_mya_core.Connection.create(
                    v+'.output1D', i_any_path+'.visibility'
                )
            else:
                if qsm_mya_core.Node.is_assembly_reference(i_any_path):
                    qsm_mya_core.Connection.create(
                        v+'.output1D', i_any_path+'.visibility'
                    )
                else:
                    i_transform_path = qsm_mya_core.Shape.get_transform(i_any_path)

                    qsm_mya_core.NodeDrawOverride.set_enable(
                        i_transform_path, True
                    )
                    qsm_mya_core.Connection.create(
                        v+'.output1D', i_transform_path+'.overrideVisibility'
                    )

    @qsm_mya_core.Undo.execute
    def execute_for_all(self):
        CameraMask.restore()

        self.restore()

        container = self.create_container()

        start_frame, end_frame = qsm_mya_core.Frame.auto_range(self._frame)
        frames = range(start_frame, end_frame+1)

        self._node_dict = {}

        all_paths = qsm_mya_core.Scene.find_all_dag_nodes(type_includes=['mesh', 'gpuCache'])
        all_path_new = self._filter_cache.generate(all_paths)
        nodes = self.nodes_pre_prc(all_path_new)

        for i_seq, i_frame in enumerate(frames):
            i_cdt_name = 'camera_mask_{}_cdt'.format(i_frame)
            qsm_mya_core.Node.create(
                i_cdt_name, 'condition'
            )
            cmds.setAttr('{}.firstTerm'.format(i_cdt_name), i_frame)
            cmds.connectAttr('time1.outTime', i_cdt_name+'.secondTerm')
            cmds.setAttr('{}.colorIfTrueR'.format(i_cdt_name), 1.0)
            cmds.setAttr('{}.colorIfFalseR'.format(i_cdt_name), 0.0)
            nodes.append(i_cdt_name)

            i_unit_conversion = qsm_mya_core.NodeAttribute.get_source_node(
                i_cdt_name, 'secondTerm', 'timeToUnitConversion'
            )
            nodes.append(i_unit_conversion)

            i_mask_nodes = self.generate_mask_nodes_at_frame(i_frame)
            i_mask_nodes_new = self._filter_cache.generate(i_mask_nodes)
            for j_shape_path in i_mask_nodes_new:
                if j_shape_path in self._node_dict:
                    j_sum_name = self._node_dict[j_shape_path]
                    nodes.append(j_sum_name)
                    qsm_mya_core.Connection.create(
                        i_cdt_name+'.outColor.outColorR', j_sum_name+'.input1D[{}]'.format(i_seq)
                    )

        qsm_mya_core.Container.add_nodes(container, list(set(nodes)))

        self.nodes_post_prc(container)


class CameraMask(object):
    LAYER_NAME = 'camera_mask_dgc'

    def __init__(self, camera=None, frame=None):
        cmds.loadPlugin('gpuCache', quiet=1)

        if camera is None:
            self._camera_path = qsm_mya_core.Camera.get_active()
        else:
            self._camera_path = qsm_mya_core.DagNode.to_path(camera)

        self._frame = frame
        self._frame_range = qsm_mya_core.Frame.auto_range(self._frame)

        self._filter_cache = _FilterCache()

    @classmethod
    def restore(cls):
        if qsm_mya_core.Node.is_exists(cls.LAYER_NAME):
            qsm_mya_core.Node.delete(
                cls.LAYER_NAME
            )

    def create_layer(self):
        layer_name = self.LAYER_NAME
        layer = qsm_mya_core.DisplayLayer.create(
            layer_name
        )
        return layer

    def generate_mask_nodes_at_frame(self, frame):
        qsm_mya_core.Frame.set_current(frame)

        results = qsm_mya_core.Camera.generate_mask_nodes(
            self._camera_path, type_includes=['mesh', 'gpuCache']
        )

        list_ = []
        for i_path in results:
            if qsm_mya_core.DagNode.is_mesh_type(i_path):
                if qsm_mya_core.Mesh.is_deformed(i_path) is False:
                    list_.append(i_path)
            else:
                list_.append(i_path)
        return list_

    @qsm_mya_core.Undo.execute
    def execute_for_all(self):
        DynamicCameraMask.restore()

        self.restore()

        layer = self.create_layer()

        mask_paths = set()
        start_frame, end_frame = self._frame_range
        frames = range(start_frame, end_frame+1)

        self._filter_cache = _FilterCache()

        all_paths = qsm_mya_core.Scene.find_all_dag_nodes(type_includes=['mesh', 'gpuCache'])
        all_path_new = self._filter_cache.generate(all_paths)

        for i_frame in frames:
            i_mask_paths = self.generate_mask_nodes_at_frame(i_frame)
            mask_paths.update(set(i_mask_paths))

        mask_paths_new = self._filter_cache.generate(mask_paths)
        hide_paths = list(set(all_path_new)-set(mask_paths_new))

        if hide_paths:
            qsm_mya_core.DisplayLayer.add_all(layer, [qsm_mya_core.Shape.get_transform(x) for x in hide_paths])
            qsm_mya_core.DisplayLayer.set_visible(layer, False)


class CameraSelection(object):
    def __init__(self, camera=None):
        if camera is None:
            self._camera_path = qsm_mya_core.Camera.get_active()
        else:
            self._camera_path = qsm_mya_core.DagNode.to_path(camera)

    @qsm_mya_core.Undo.execute
    def execute(self):
        shape_paths = qsm_mya_core.Camera.generate_mask_nodes(
            self._camera_path, type_includes=['mesh', 'gpuCache']
        )
        list_ = []
        for i in shape_paths:
            i_result = _core.Assembly.find_any_by_shape(i)
            if i_result is not None:
                list_.append(i_result)

        qsm_mya_core.Selection.set(list_)


class CameraLodSwitch(object):
    def __init__(self, camera=None, frame=None):
        if camera is None:
            self._camera_path = qsm_mya_core.Camera.get_active()
        else:
            self._camera_path = qsm_mya_core.DagNode.to_path(camera)

        self._frame = frame
        self._frame_range = qsm_mya_core.Frame.auto_range(self._frame)

    def generate_mask_nodes_at_frame(self, frame):
        qsm_mya_core.Frame.set_current(frame)

        shape_paths = qsm_mya_core.Camera.generate_mask_nodes(
            self._camera_path, type_includes=['mesh', 'gpuCache']
        )
        list_ = []
        for i in shape_paths:
            i_result = _core.Assembly.find_any_by_shape(i)
            if i_result is not None:
                list_.append(i_result)
        return list_

    @qsm_mya_core.Undo.execute
    def execute(self, distance_range=(50, 100)):
        dict_ = {}
        camera_transform = qsm_mya_core.Shape.get_transform(self._camera_path)
        start_frame, end_frame = self._frame_range
        frames = range(start_frame, end_frame+1)
        for i_frame in frames:
            i_mask_paths = self.generate_mask_nodes_at_frame(i_frame)
            i_camera_point = qsm_mya_core.Transform.get_world_center(camera_transform)
            for j_node in i_mask_paths:
                j_node_point = qsm_mya_core.Transform.get_world_center(j_node)
                j_distance = qsm_mya_core.Transform.compute_distance(i_camera_point, j_node_point)

                dict_.setdefault(
                    j_node, set()
                ).add(j_distance)

        lod_dict = {}

        for k, v in dict_.items():
            i_distance = min(v)
            if distance_range[0] > i_distance:
                i_lod = 0
            elif distance_range[0] < i_distance < distance_range[1]:
                i_lod = 1
            else:
                i_lod = 2

            lod_dict[k] = i_lod
            i_qsm_type = qsm_mya_core.NodeAttribute.get_value(
                k, 'qsm_type'
            )
            if i_qsm_type == 'unit_assembly':
                i_opt = _core.UnitAssemblyOpt(k)
                i_opt.set_lod(i_lod)
            elif i_qsm_type == 'gpu_instance':
                i_opt = _core.GpuInstanceOpt(k)
                i_opt.set_lod(i_lod)


class CameraMaskOpt(object):
    @classmethod
    def create_auto(cls, **kwargs):
        scheme = kwargs['scheme']
        if scheme == 'default':
            camera = qsm_mya_core.Camera.get_active()
            CameraMask(camera).execute_for_all()
        elif scheme == 'dynamic':
            camera = qsm_mya_core.Camera.get_active()
            DynamicCameraMask(camera).execute_for_all()

    @classmethod
    def remove_auto(cls, **kwargs):
        DynamicCameraMask.restore()
        CameraMask.restore()
