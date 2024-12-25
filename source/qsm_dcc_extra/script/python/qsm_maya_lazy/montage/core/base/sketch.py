# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_maya.core as qsm_mya_core


class Sketch(object):
    def __init__(self, path):
        self._path = path

    def get_data(self, key_includes):
        dict_ = {}
        for i_atr_name in key_includes:
            dict_[i_atr_name] = cmds.getAttr(self._path+'.'+i_atr_name)
        return dict_

    def get_rotation_between(self, path_upper):
        keys = [
            'rotateX', 'rotateY', 'rotateZ'
        ]
        a = self._path[len(path_upper)+1:]
        _ = a.split('|')
        c = len(_)
        data = []
        for i in range(c):
            i_path = '{}|{}'.format(path_upper, '|'.join(_[:i+1]))
            data.append(
                cmds.xform(i_path, rotation=1, worldSpace=0, query=1)
            )
        return {
            keys[idx]: sum(x) for idx, x in enumerate(zip(*data))
        }

    def get_orients(self):
        dict_ = {}
        for i_atr_name in [
            'rotateOrder',
            'jointOrientX',
            'jointOrientY',
            'jointOrientZ',
        ]:
            dict_[i_atr_name] = cmds.getAttr(self._path+'.'+i_atr_name)
        return dict_

    def apply_orients(self, orient):
        for k, v in orient.items():
            cmds.setAttr(
                self._path+'.'+k, v
            )

    def apply_rotations(self, rotations):
        pass

    def create_point_constraint_to_master_layer(self, target_node):
        # when is created, connect to exists
        results = qsm_mya_core.PointConstraint.get_all_from_source(target_node)
        if results:
            node = results[0]
            next_index = qsm_mya_core.PointConstraint.get_next_index(node)
            cmds.connectAttr(
                self._path+'.translate', node+'.target[{}].targetTranslate'.format(next_index)
            )
            cmds.connectAttr(
                self._path+'.rotatePivot', node+'.target[{}].targetRotatePivot'.format(next_index)
            )
            cmds.connectAttr(
                self._path+'.rotatePivotTranslate', node+'.target[{}].targetRotateTranslate'.format(next_index)
            )
            cmds.connectAttr(
                self._path+'.parentMatrix[0]', node+'.target[{}].targetParentMatrix'.format(next_index)
            )
            return node
        else:
            _ = cmds.pointConstraint(
                self._path, target_node,
                # maintainOffset=1, weight=1
            )
            node = _[0]
            return node

    def create_orient_constraint_to_master_layer(self, target_node):
        # when is created, connect to exists
        results = qsm_mya_core.OrientConstraint.get_all_from_source(target_node)
        if results:
            node = results[0]
            next_index = qsm_mya_core.OrientConstraint.get_next_index(node)
            cmds.connectAttr(
                self._path+'.rotate', node+'.target[{}].targetRotate'.format(next_index)
            )
            cmds.connectAttr(
                self._path+'.jointOrient', node+'.target[{}].targetJointOrient'.format(next_index)
            )
            cmds.connectAttr(
                self._path+'.rotateOrder', node+'.target[{}].targetRotateOrder'.format(next_index)
            )
            cmds.connectAttr(
                self._path+'.parentMatrix[0]', node+'.target[{}].targetParentMatrix'.format(next_index)
            )
            return node
        else:
            _ = cmds.orientConstraint(
                self._path, target_node, maintainOffset=1, weight=1
            )
            node = _[0]
            cmds.setAttr(node+'.interpType', 2)
            for i in [
                'offsetX',
                'offsetY',
                'offsetZ'
            ]:
                cmds.setAttr(
                    node+'.'+i, 0
                )
            return node

    def create_point_constraint_to_resource(self, target_node):
        _ = cmds.pointConstraint(
            self._path, target_node,
            # maintainOffset=1, weight=1
        )
        node = _[0]
        return node

    def create_orient_constraint_to_resource(self, target_node, clear_offset=True):
        _ = cmds.orientConstraint(
            self._path, target_node, maintainOffset=1, weight=1
        )
        node = _[0]
        cmds.setAttr(node+'.interpType', 2)
        if clear_offset is True:
            for i in [
                'offsetX',
                'offsetY',
                'offsetZ'
            ]:
                cmds.setAttr(
                    node+'.'+i, 0
                )
        return node

    def reset_rotations(self):
        for i in [
            'rotateX', 'rotateY', 'rotateZ'
        ]:
            cmds.setAttr(self._path+'.'+i, 0)

    def reset_translations(self):
        for i in [
            'translateX', 'translateY', 'translateZ',
        ]:
            cmds.setAttr(self._path+'.'+i, 0)

    def match_translations_from(self, source_node):
        for i in [
            'translateX', 'translateY', 'translateZ',
        ]:
            cmds.setAttr(
                self._path+'.'+i,
                cmds.getAttr(source_node+'.'+i)
            )

    def match_rotations_from(self, source_node):
        for i in [
            'rotateX', 'rotateY', 'rotateZ'
        ]:
            cmds.setAttr(
                self._path+'.'+i,
                cmds.getAttr(source_node+'.'+i)
            )

    def match_orients_from(self, source_node):
        for i in [
            'jointOrientX',
            'jointOrientY',
            'jointOrientZ'
        ]:
            cmds.setAttr(
                self._path+'.'+i,
                cmds.getAttr(source_node+'.'+i)
            )

    def match_all_from(self, source_node):
        self.match_rotations_from(source_node)
        self.match_orients_from(source_node)

    @classmethod
    def test(cls):
        print cls(
            qsm_mya_core.DagNode.to_path('sam_Skin:Elbow_R')
        ).get_rotation_between(
            qsm_mya_core.DagNode.to_path('sam_Skin:Shoulder_R')
        )
