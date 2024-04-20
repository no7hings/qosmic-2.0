# coding:utf-8
import os

import math
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxcontent.core as ctt_core

import qsm_maya.asset.core as qsm_mya_ast_core

import lxresource as bsc_resource

import qsm_maya.rig.core as qsm_rig_core

import lxbasic.core as bsc_core

import lxmaya.dcc.objects as mya_dcc_objects


class AdvSkinProxyGenerate(object):
    MAIN_KEYS = [
        'root',
        'spine',
        'chest',
        'neck',
        'head',
        'head_end',
        #
        'scapula',
        'shoulder',
        'elbow',
        'wrist',
        'finger',
        'finger_end',
        #
        'hip',
        'knee',
        'ankle',
        'toes',
        'toes_end',
    ]

    ERROR_KEYS = [
        ''
    ]

    PROXY_CONTROL_PATH = '|__skin_proxy_control__'
    PROXY_GEOMETRY_GROUP_PATH = '|__skin_proxy_geo_grp__'

    CACHE_ROOT = '|__SKIN_PROXY__'

    CACHE_NAME = qsm_rig_core.RigConfigure.SkinProxyCacheName

    @classmethod
    def _create_group(cls, path):
        if cmds.objExists(path) is False:
            _ = path.split('|')
            parent_path = '|'.join(_[:-1])
            name = _[-1]
            cmds.createNode(
                'transform', name=name, parent=parent_path or None, skipSelect=1
            )

    @classmethod
    def _copy_control(cls, root, path, scale_x=False, scale_y=False):
        nodes = []
        if cmds.objExists(path) is False:
            _ = path.split('|')
            parent_path = '|'.join(_[:-1])
            name = _[-1]

            results = cmds.duplicate(
                cls.PROXY_CONTROL_PATH, name=name,
            )
            transform_path = results[0]
            # nodes.append(transform_path)
            shape_paths = cmds.listRelatives(transform_path, children=1, shapes=1, noIntermediate=1, fullPath=1)
            xyz = ['x', 'y', 'z']
            for i_seq, i_shape_path in enumerate(shape_paths):
                i_shape_name = '{}_{}_Shape'.format(name, xyz[i_seq])
                cmds.rename(i_shape_path, i_shape_name)
                i_shape_path_new = '{}|{}'.format(transform_path, i_shape_name)
                cmds.connectAttr(
                    '{}.qsm_locator_visibility'.format(root),
                    '{}.visibility'.format(i_shape_path_new)
                )
                # nodes.append(i_shape_path_new)

            cmds.addAttr(
                transform_path, longName='qsm_scale', attributeType='double', keyable=1, defaultValue=1.0
            )
            cmds.addAttr(
                transform_path, longName='qsm_scale_weight', attributeType='double', keyable=1, defaultValue=1.0
            )
            multiply_name = '{}_mtp'.format(name)
            multiply = cmds.createNode('multiplyDivide', name=multiply_name, skipSelect=1)
            nodes.append(multiply)
            cmds.connectAttr(
                '{}.qsm_scale'.format(transform_path), '{}.input1X'.format(multiply)
            )
            cmds.connectAttr(
                '{}.qsm_scale_weight'.format(transform_path), '{}.input2X'.format(multiply)
            )
            if scale_x is True:
                cmds.connectAttr(
                    '{}.output.outputX'.format(multiply), '{}.scale.scaleX'.format(transform_path)
                )

            if scale_y is True:
                cmds.connectAttr(
                    '{}.output.outputX'.format(multiply), '{}.scale.scaleY'.format(transform_path)
                )

            cmds.parent(transform_path, parent_path)
            return nodes

    @classmethod
    def _get_parent_constrains(cls, path):
        return list(
            set(
                cmds.listConnections(
                    path, destination=0, source=1, type='parentConstraint'
                ) or []
            )
        )

    @classmethod
    def _get_scale_constrains(cls, path):
        return list(
            set(
                cmds.listConnections(
                    path, destination=0, source=1, type='scaleConstraint'
                ) or []
            )
        )

    @classmethod
    def _clear_constrains(cls, path):
        _ = cls._get_parent_constrains(path)
        if _:
            for i in _:
                cmds.delete(i)

    @classmethod
    def _clear_all_constrains(cls, root):
        for i in cmds.ls(root, dag=1, type='parentConstraint'):
            cmds.delete(i)

    @classmethod
    def _break_all_constrains(cls, root):
        [cls._disconnect_parent_constrain(i) for i in cmds.ls(root, dag=1, type='parentConstraint')]
        [cls._disconnect_scale_constrain(i) for i in cmds.ls(root, dag=1, type='scaleConstraint')]

    @classmethod
    def _disconnect_parent_constrain(cls, constrain_path):
        ps_dst = [
            'target[0].targetParentMatrix',
            'target[0].targetTranslate',
            'target[0].targetRotatePivot',
            'target[0].targetRotateTranslate',
            'target[0].targetRotate',
            'target[0].targetRotateOrder',
            'target[0].targetJointOrient',
            'target[0].targetScaleCompensate',
            'target[0].targetInverseScale',
            'target[0].targetScale'
        ]
        for i in ps_dst:
            i_tgt = '{}.{}'.format(constrain_path, i)
            i_src = cmds.connectionInfo(
                i_tgt,
                sourceFromDestination=1
            )
            if i_src:
                cmds.disconnectAttr(i_src, i_tgt)

    @classmethod
    def _disconnect_scale_constrain(cls, constrain_path):
        ps_dst = [
            'target[0].targetParentMatrix',
            'target[0].targetScale',
        ]
        for i in ps_dst:
            i_tgt = '{}.{}'.format(constrain_path, i)
            i_src = cmds.connectionInfo(
                i_tgt,
                sourceFromDestination=1
            )
            if i_src:
                cmds.disconnectAttr(i_src, i_tgt)

    @classmethod
    def _connect_parent_constrain(cls, path, constrain_path):
        cs = [
            ('parentMatrix[0]', 'target[0].targetParentMatrix'),
            ('translate', 'target[0].targetTranslate'),
            ('rotatePivot', 'target[0].targetRotatePivot'),
            ('rotatePivotTranslate', 'target[0].targetRotateTranslate'),
            ('rotate', 'target[0].targetRotate'),
            ('rotateOrder', 'target[0].targetRotateOrder'),
            ('jointOrient', 'target[0].targetJointOrient'),
            ('segmentScaleCompensate', 'target[0].targetScaleCompensate'),
            ('inverseScale', 'target[0].targetInverseScale'),
            ('scale', 'target[0].targetScale'),
        ]
        for i_src, i_dst in cs:
            cmds.connectAttr(
                '{}.{}'.format(path, i_src), '{}.{}'.format(constrain_path, i_dst)
            )

    @classmethod
    def _connect_scale_constrain(cls, path, constrain_path):
        cs = [
            ('parentMatrix[0]', 'target[0].targetParentMatrix'),
            ('scale', 'target[0].targetScale'),
        ]
        for i_src, i_dst in cs:
            cmds.connectAttr(
                '{}.{}'.format(path, i_src), '{}.{}'.format(constrain_path, i_dst)
            )

    @classmethod
    def _compute_distance(cls, path, path_dst):
        x, y, z = cmds.getAttr('{}.translate'.format(path))[0]
        x_dst, y_dst, z_dst = cmds.getAttr('{}.translate'.format(path_dst))[0]
        return math.sqrt((x-x_dst)**2+(y-y_dst)**2+(z-z_dst)**2)

    @classmethod
    def _save_distance(cls, path, distance):
        atr_path = '{}.qsm_distance'.format(path)
        if cmds.objExists(atr_path) is False:
            cmds.addAttr(path, longName='qsm_distance', attributeType='double', keyable=1)

        cmds.setAttr(atr_path, distance)

    @classmethod
    def _save_height(cls, path, height):
        atr_path = '{}.qsm_height'.format(path)
        if cmds.objExists(atr_path) is False:
            cmds.addAttr(path, longName='qsm_height', attributeType='double', keyable=1)

        cmds.setAttr(atr_path, height)

    @classmethod
    def _save_target_offset(cls, path, translate, rotate):
        translate_atr_path = '{}.qsm_offset_translate'.format(path)
        cmds.addAttr(
            path, longName='qsm_offset_translate', attributeType='double3', keyable=1
        )
        cmds.addAttr(
            path, longName='qsm_offset_translateX', attributeType='double', parent='qsm_offset_translate', keyable=1
        )
        cmds.addAttr(
            path, longName='qsm_offset_translateY', attributeType='double', parent='qsm_offset_translate', keyable=1
        )
        cmds.addAttr(
            path, longName='qsm_offset_translateZ', attributeType='double', parent='qsm_offset_translate', keyable=1
        )
        cmds.setAttr(translate_atr_path, *translate)

        rotate_atr_path = '{}.qsm_offset_rotate'.format(path)
        cmds.addAttr(
            path, longName='qsm_offset_rotate', attributeType='double3', keyable=1
        )
        cmds.addAttr(
            path, longName='qsm_offset_rotateX', attributeType='double', parent='qsm_offset_rotate', keyable=1
        )
        cmds.addAttr(
            path, longName='qsm_offset_rotateY', attributeType='double', parent='qsm_offset_rotate', keyable=1
        )
        cmds.addAttr(
            path, longName='qsm_offset_rotateZ', attributeType='double', parent='qsm_offset_rotate', keyable=1
        )
        cmds.setAttr(rotate_atr_path, *rotate)

    @classmethod
    def _load_target_offset(cls, path, translate, rotate):
        cmds.setAttr('{}.target[0].targetOffsetTranslate'.format(path), *translate)
        cmds.setAttr('{}.target[0].targetOffsetRotate'.format(path), *rotate)

    @classmethod
    def _copy_geometry(cls, path, name_src):
        if cmds.objExists(path) is False:
            _ = path.split('|')
            parent_path = '|'.join(_[:-1])
            name = _[-1]
            path_src = '|__skin_proxy_geo_grp__|{}'.format(name_src)
            if cmds.objExists(path_src) is True:
                results = cmds.duplicate(
                    path_src, name=name,
                )
                transform_path = results[0]
                cmds.parent(transform_path, parent_path)

                need_reverse = cmds.getAttr('{}.scaleX'.format(path_src)) < 0

                cmds.makeIdentity(path, apply=1, translate=1, rotate=1, scale=1)
                cmds.makeIdentity(path, apply=0, translate=1, rotate=1, scale=1)

                if need_reverse is True:
                    shape_paths = cmds.listRelatives(path, children=1, shapes=1, noIntermediate=1, fullPath=1)
                    for i_shape_path in shape_paths:
                        cmds.polyNormal(i_shape_path, normalMode=0, userNormalMode=0, ch=0)

    @classmethod
    def _import_file(cls, file_path, namespace=':'):
        return cmds.file(
            file_path,
            i=True,
            options='v=0;',
            type='mayaAscii',
            ra=True,
            mergeNamespacesOnClash=True,
            namespace=namespace,
        )

    def __init__(self, namespace):
        self._namespace = namespace
        self._adv_query = qsm_rig_core.AdvQuery(namespace)

    def create_cache_root_auto(self):
        if cmds.objExists(self.CACHE_ROOT) is False:
            cmds.createNode(
                'dagContainer', name=self.CACHE_ROOT.split('|')[-1], shared=1, skipSelect=1
            )
            cmds.setAttr(self.CACHE_ROOT+'.iconName', 'folder-closed.png', type='string')

    def hide_geometry_root(self, namespace):
        if namespace is not None:
            root_path = '|{}:{}'.format(namespace, self.CACHE_NAME)
        else:
            root_path = '|{}'.format(self.CACHE_NAME)

        geometry_roots = self._adv_query.main_query.get('geometry_root')
        if geometry_roots:
            layer_name = '{}_geometry_hide'.format(self._namespace)
            if cmds.objExists(layer_name) is False:
                layer = cmds.createDisplayLayer(name=layer_name, number=1, empty=True)
                cmds.editDisplayLayerMembers(layer, *geometry_roots)
                cmds.setAttr(layer + '.visibility', False)

                if namespace is not None:
                    dgc_path = '{}|{}:skin_proxy_dgc'.format(root_path, namespace)
                else:
                    dgc_path = '{}|skin_proxy_dgc'.format(root_path)

                cmds.container(dgc_path, edit=1, force=1, addNode=[layer])

    def hide_source_geometry_root(self, location):
        geometry_roots = self._adv_query.main_query.get('geometry_root')
        if geometry_roots:
            layer_name = '{}_skin_proxy_hide'.format(self._namespace)
            layer_path = cmds.createDisplayLayer(name=layer_name, number=1, empty=True)
            cmds.editDisplayLayerMembers(layer_path, *geometry_roots)
            cmds.setAttr(layer_path + '.visibility', False)

            cmds.container(location, edit=1, force=1, addNode=[layer_path])

    def create_resource_controls(self, location):
        if cmds.objExists(self.PROXY_CONTROL_PATH) is False:
            self._import_file(bsc_resource.ExtendResource.get('rig/skin_proxy_control.ma'))

        parent_path = '|'.join(location.split('|')[:-1])
        name = location.split('|')[-1]
        cmds.container(type='dagContainer', name=name)
        if parent_path:
            cmds.parent(name, parent_path)

        cmds.setAttr(location + '.iconName', 'fileNew.png', type='string')

        cmds.addAttr(
            location, longName='qsm_scale_weight', attributeType='double', keyable=1, defaultValue=1.0
        )
        cmds.addAttr(
            location, longName='qsm_locator_visibility', attributeType='long', keyable=1
        )
        cmds.addAttr(location, longName='qsm_cache', dataType='string')

        nodes = []

        leaf_keys = self._adv_query.skeleton_query.get_all_leaf_keys()
        for i_main_key in self.MAIN_KEYS:
            i_keys = ctt_core.ContentUtil.filter(leaf_keys, '{}.*'.format(i_main_key))
            for j_key in i_keys:
                j_key_path = j_key.replace('.', '_')
                j_group_path = '{}|{}_grp'.format(location, j_key_path)
                j_control_path = '{}|{}_ctl'.format(j_group_path, j_key_path)
                self._create_group(j_group_path)
                if j_key in ['ankle.L', 'ankle.R', 'toes.L', 'toes.R']:
                    j_nodes = self._copy_control(location, j_control_path, scale_x=True)
                else:
                    j_nodes = self._copy_control(location, j_control_path, scale_x=True, scale_y=True)

                nodes.extend(j_nodes)

                cmds.connectAttr(
                    '{}.qsm_scale_weight'.format(location), '{}.qsm_scale_weight'.format(j_control_path)
                )

        cmds.container(location, edit=1, force=1, addNode=nodes)

        cmds.delete(self.PROXY_CONTROL_PATH)

    def match_resource_positions(self, location):
        leaf_keys = self._adv_query.skeleton_query.get_all_leaf_keys()
        for i_main_key in self.MAIN_KEYS:
            i_keys = ctt_core.ContentUtil.filter(leaf_keys, '{}.*'.format(i_main_key))
            for j_key in i_keys:
                j_skeleton_paths = self._adv_query.skeleton_query.get(j_key)
                if not j_skeleton_paths:
                    continue

                j_key_path = j_key.replace('.', '_')
                j_group_path = '{}|{}_grp'.format(location, j_key_path)
                j_control_path = '{}|{}_ctl'.format(j_group_path, j_key_path)

                j_skeleton_path = j_skeleton_paths[0]
                if not self._get_parent_constrains(j_group_path):
                    cmds.parentConstraint(j_skeleton_path, j_group_path)

                j_geo_rotation = self._adv_query.rotation_query.get(j_key)
                cmds.setAttr('{}.rotate'.format(j_control_path), *j_geo_rotation)

        self._clear_all_constrains(location)

    def match_resource_distance(self, location):
        head_end_key = 'head_end.M'
        head_end_key_path = head_end_key.replace('.', '_')

        head_end_group_path = '{}|{}_grp'.format(location, head_end_key_path)

        height = cmds.getAttr('{}.translateY'.format(head_end_group_path))
        self._save_height(location, height)

        leaf_keys = self._adv_query.skeleton_query.get_all_leaf_keys()
        for i_main_key in self.MAIN_KEYS:
            i_keys = ctt_core.ContentUtil.filter(leaf_keys, '{}.*'.format(i_main_key))
            for j_key in i_keys:
                j_skeleton_paths = self._adv_query.skeleton_query.get(j_key)
                if not j_skeleton_paths:
                    continue

                j_key_path = j_key.replace('.', '_')

                j_group_path = '{}|{}_grp'.format(location, j_key_path)

                j_control_path = '{}|{}_ctl'.format(j_group_path, j_key_path)

                j_control_z_shape_path = '{}|{}_ctl_z_Shape'.format(j_control_path, j_key_path)

                j_key_dst = self._adv_query.distance_query.get(j_key)
                if not j_key_dst:
                    continue

                j_key_path_dst = j_key_dst.replace('.', '_')
                j_group_path_dst = '{}|{}_grp'.format(location, j_key_path_dst)

                j_distance = self._compute_distance(j_group_path, j_group_path_dst)

                self._save_distance(j_group_path, j_distance)

                cmds.setAttr(
                    '{}.localPositionZ'.format(j_control_z_shape_path), j_distance/2
                )
                cmds.setAttr(
                    '{}.localScaleZ'.format(j_control_z_shape_path), j_distance/2
                )

    def create_resource_geometries(self, location):
        if cmds.objExists(self.PROXY_GEOMETRY_GROUP_PATH) is False:
            if qsm_rig_core.SCHEME == 'new':
                self._import_file(bsc_resource.ExtendResource.get('rig/skin_proxy_geometry_new.ma'))
            else:
                self._import_file(bsc_resource.ExtendResource.get('rig/skin_proxy_geometry.ma'))

        leaf_keys = self._adv_query.skeleton_query.get_all_leaf_keys()
        for i_main_key in self.MAIN_KEYS:
            i_keys = ctt_core.ContentUtil.filter(leaf_keys, '{}.*'.format(i_main_key))
            for j_key in i_keys:
                j_skeleton_paths = self._adv_query.skeleton_query.get(j_key)
                if not j_skeleton_paths:
                    continue

                j_key_path = j_key.replace('.', '_')
                j_group_path = '{}|{}_grp'.format(location, j_key_path)

                j_control_path = '{}|{}_ctl'.format(j_group_path, j_key_path)

                j_geo_path = '{}|{}_geo_copy'.format(j_control_path, j_key_path)

                j_geo_name_src = self._adv_query.geometry_query.get(j_key)

                self._copy_geometry(j_geo_path, j_geo_name_src)

        cmds.delete(self.PROXY_GEOMETRY_GROUP_PATH)

    # resource
    def build_resource(self):
        location = '|{}'.format(self.CACHE_NAME)
        self.create_resource_controls(location)
        self.match_resource_positions(location)
        self.match_resource_distance(location)
        self.create_resource_geometries(location)

    # create cache
    def create_cache(self, cache_file_path=None):
        location = '|{}'.format(self.CACHE_NAME)
        if cmds.objExists(location) is False:
            if qsm_rig_core.SCHEME == 'new':
                self._import_file(
                    bsc_resource.ExtendResource.get('rig/skin_proxy_new.ma')
                )
            else:
                self._import_file(
                    bsc_resource.ExtendResource.get('rig/skin_proxy.ma')
                )

        self.match_cache_positions(location)
        self.match_cache_sizes(location)
        cmds.setAttr(location + '.blackBox', 1, lock=1)

        if cache_file_path is None:
            file_path = qsm_mya_ast_core.NamespaceQuery().get_file(self._namespace)
            cache_file_path = qsm_mya_ast_core.AssetCache.get_skin_proxy_file(
                file_path
            )

        bsc_core.StgBaseMtd.create_directory(
            os.path.dirname(cache_file_path)
        )

        mya_dcc_objects.Scene.export_to_file(
            cache_file_path, location
        )

    def match_cache_positions(self, location):
        root_skeleton_paths = self._adv_query.skeleton_query.get('root.M')
        cmds.scaleConstraint(root_skeleton_paths[0], location)
        leaf_keys = self._adv_query.skeleton_query.get_all_leaf_keys()
        for i_main_key in self.MAIN_KEYS:
            i_keys = ctt_core.ContentUtil.filter(leaf_keys, '{}.*'.format(i_main_key))
            for j_key in i_keys:
                j_skeleton_paths = self._adv_query.skeleton_query.get(j_key)
                if not j_skeleton_paths:
                    continue

                j_key_path = j_key.replace('.', '_')
                j_group_path = '{}|{}_grp'.format(location, j_key_path)
                j_constraint_name = '{}_cst'.format(j_key_path)
                j_skeleton_path = j_skeleton_paths[0]
                if not self._get_parent_constrains(j_group_path):
                    if j_key in ['ankle.L']:
                        j_value_pre = cmds.getAttr('{}.translateY'.format(j_group_path))
                        j_constraints = cmds.parentConstraint(j_skeleton_path, j_group_path)
                        j_value = cmds.getAttr('{}.translateY'.format(j_group_path))
                        j_offset = j_value_pre - j_value
                        cmds.setAttr('{}.target[0].targetOffsetTranslateX'.format(j_constraints[0]), j_offset)
                        self._save_target_offset(
                            j_group_path, (j_offset, 0, 0), (0, 0, 0)
                        )
                    elif j_key in ['ankle.R']:
                        j_value_pre = cmds.getAttr('{}.translateY'.format(j_group_path))
                        j_constraints = cmds.parentConstraint(j_skeleton_path, j_group_path)
                        j_value = cmds.getAttr('{}.translateY'.format(j_group_path))
                        j_offset = -(j_value_pre - j_value)
                        cmds.setAttr('{}.target[0].targetOffsetTranslateX'.format(j_constraints[0]), j_offset)
                        self._save_target_offset(
                            j_group_path, (j_offset, 0, 0), (0, 0, 0)
                        )
                    elif j_key in ['toes.L']:
                        j_value_pre = cmds.getAttr('{}.translateY'.format(j_group_path))
                        j_value_pre_1 = cmds.getAttr('{}.rotateY'.format(j_group_path))
                        j_constraints = cmds.parentConstraint(j_skeleton_path, j_group_path)
                        j_value = cmds.getAttr('{}.translateY'.format(j_group_path))
                        j_value_1 = cmds.getAttr('{}.rotateY'.format(j_group_path))

                        j_offset = -(j_value_pre - j_value)
                        cmds.setAttr('{}.target[0].targetOffsetTranslateY'.format(j_constraints[0]), j_offset)

                        j_offset_1 = j_value_pre_1 - j_value_1
                        cmds.setAttr('{}.target[0].targetOffsetRotateZ'.format(j_constraints[0]), j_offset_1)
                        self._save_target_offset(
                            j_group_path, (0, j_offset, 0), (0, 0, j_offset_1)
                        )
                    elif j_key in ['toes.R']:
                        j_value_pre = cmds.getAttr('{}.translateY'.format(j_group_path))
                        j_value_pre_1 = cmds.getAttr('{}.rotateY'.format(j_group_path))
                        j_constraints = cmds.parentConstraint(j_skeleton_path, j_group_path)
                        j_value = cmds.getAttr('{}.translateY'.format(j_group_path))
                        j_value_1 = cmds.getAttr('{}.rotateY'.format(j_group_path))

                        j_offset = j_value_pre - j_value
                        cmds.setAttr('{}.target[0].targetOffsetTranslateY'.format(j_constraints[0]), j_offset)

                        j_offset_1 = -(j_value_pre_1 - j_value_1)
                        cmds.setAttr('{}.target[0].targetOffsetRotateZ'.format(j_constraints[0]), j_offset_1)
                        self._save_target_offset(
                            j_group_path, (0, j_offset, 0), (0, 0, j_offset_1)
                        )
                    else:
                        j_constraints = cmds.parentConstraint(j_skeleton_path, j_group_path)
                        self._save_target_offset(
                            j_group_path, (0, 0, 0), (0, 0, 0)
                        )
                    #
                    if j_constraints:
                        cmds.rename(j_constraints[0], j_constraint_name)

        self._break_all_constrains(location)

    def match_cache_sizes(self, location):
        head_end_key = 'head_end.M'
        head_end_key_path = head_end_key.replace('.', '_')

        head_end_group_path = '{}|{}_grp'.format(location, head_end_key_path)

        height_new = cmds.getAttr('{}.translateY'.format(head_end_group_path))
        height_old = cmds.getAttr('{}.qsm_height'.format(location))
        scale = height_new / height_old

        leaf_keys = self._adv_query.skeleton_query.get_all_leaf_keys()
        for i_main_key in self.MAIN_KEYS:
            i_keys = ctt_core.ContentUtil.filter(leaf_keys, '{}.*'.format(i_main_key))
            for j_key in i_keys:
                j_skeleton_paths = self._adv_query.skeleton_query.get(j_key)
                if not j_skeleton_paths:
                    continue

                j_key_path = j_key.replace('.', '_')

                j_group_path = '{}|{}_grp'.format(location, j_key_path)

                j_control_path = '{}|{}_ctl'.format(j_group_path, j_key_path)

                j_key_dst = self._adv_query.distance_query.get(j_key)
                if not j_key_dst:
                    continue

                j_key_path_dst = j_key_dst.replace('.', '_')
                j_group_path_dst = '{}|{}_grp'.format(location, j_key_path_dst)

                j_distance_new = self._compute_distance(j_group_path, j_group_path_dst)
                j_distance_old = cmds.getAttr('{}.qsm_distance'.format(j_group_path))

                j_scale = j_distance_new / j_distance_old

                cmds.setAttr('{}.qsm_scale'.format(j_control_path), scale)
                cmds.setAttr('{}.scaleZ'.format(j_control_path), j_scale)

    def load_cache_constrains(self, namespace=None):
        if namespace is not None:
            root_path = '|{}:{}'.format(namespace, self.CACHE_NAME)
        else:
            root_path = '|{}'.format(self.CACHE_NAME)

        leaf_keys = self._adv_query.skeleton_query.get_all_leaf_keys()
        for i_main_key in self.MAIN_KEYS:
            i_keys = ctt_core.ContentUtil.filter(leaf_keys, '{}.*'.format(i_main_key))
            for j_key in i_keys:
                j_skeleton_paths = self._adv_query.skeleton_query.get(j_key)
                if not j_skeleton_paths:
                    continue

                j_key_path = j_key.replace('.', '_')
                if namespace is not None:
                    j_group_path = '{}|{}:{}_grp'.format(root_path, namespace, j_key_path)
                else:
                    j_group_path = '{}|{}_grp'.format(root_path, j_key_path)

                j_skeleton_path = j_skeleton_paths[0]
                if not self._get_parent_constrains(j_group_path):
                    j_constraints = cmds.parentConstraint(j_skeleton_path, j_group_path)
                    self._load_target_offset(
                        j_constraints[0],
                        cmds.getAttr('{}.qsm_offset_translate'.format(j_group_path))[0],
                        cmds.getAttr('{}.qsm_offset_rotate'.format(j_group_path))[0]
                    )

    def connect_cache_constrains(self, location, namespace):
        root_skeleton_paths = self._adv_query.skeleton_query.get('root.M')
        scale_constrains = self._get_scale_constrains(location)

        self._connect_scale_constrain(root_skeleton_paths[0], scale_constrains[0])

        leaf_keys = self._adv_query.skeleton_query.get_all_leaf_keys()
        for i_main_key in self.MAIN_KEYS:
            i_keys = ctt_core.ContentUtil.filter(leaf_keys, '{}.*'.format(i_main_key))
            for j_key in i_keys:
                j_skeleton_paths = self._adv_query.skeleton_query.get(j_key)
                if not j_skeleton_paths:
                    continue

                j_key_path = j_key.replace('.', '_')
                j_group_path = '{}|{}:{}_grp'.format(location, namespace, j_key_path)

                j_constrains = self._get_parent_constrains(j_group_path)
                if not j_constrains:
                    continue

                self._connect_parent_constrain(j_skeleton_paths[0], j_constrains[0])

    def load_cache(self, cache_file_path):
        self.create_cache_root_auto()

        namespace = self._namespace

        cache_location_new = '{}|{}:{}'.format(self.CACHE_ROOT, self._namespace, self.CACHE_NAME)
        cache_location = '|{}:{}'.format(namespace, self.CACHE_NAME)
        if cmds.objExists(cache_location) is False and cmds.objExists(cache_location_new) is False:
            if os.path.isfile(cache_file_path) is True:
                self._import_file(
                    cache_file_path, namespace=namespace
                )
                self.connect_cache_constrains(cache_location, namespace)

                self.auto_hide(cache_location)

                cmds.parent(cache_location, self.CACHE_ROOT)

    def auto_hide(self, location):
        self.hide_source_geometry_root(location)

    def generate_args(self):
        file_path = qsm_mya_ast_core.NamespaceQuery().get_file(self._namespace)
        cache_file_path = qsm_mya_ast_core.AssetCache.get_skin_proxy_file(
            file_path
        )
        if os.path.isfile(cache_file_path) is False:
            cmd = qsm_mya_ast_core.MayaCacheProcess.generate_command(
                'method=skin-proxy-cache-generate&file={}&cache_file={}'.format(
                    file_path,
                    cache_file_path,
                )
            )
            return cmd, cache_file_path
        return None, cache_file_path

    def test(self):
        pass


class AdvSkinProxyProcess(object):
    def __init__(self, file_path, cache_file_path):
        self._file_path = file_path
        self._cache_file_path = cache_file_path

    def execute(self):
        namespace = 'skin_proxy'
        mya_dcc_objects.Scene.new_file()
        mya_dcc_objects.Scene.reference_file_from(
            self._file_path, namespace=namespace
        )
        AdvSkinProxyGenerate(namespace).create_cache(
            self._cache_file_path
        )
