# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import lxbasic.log as bsc_log

from . import node as _node

from . import attribute as _attribute

from . import node_for_transform as _node_for_transform

from . import shape as _shape


class RebuildForNucleus(object):
    @classmethod
    def create_for(cls, node_type, target_shape_path, target_any_paths):
        """
        nClothCreate;
        performCreateNCloth 0;
        createNCloth 0;
        sets -e -forceElement initialShadingGroup;
        """
        target_any_paths = [
            _shape.Shape.get_transform(x) if _shape.Shape.check_is_shape(x) else x
            for x in target_any_paths
        ]
        cmds.select(target_any_paths)

        if _node_for_transform.Transform.is_transform_type(target_shape_path):
            target_shape_path = _node_for_transform.Transform.get_shape(target_shape_path)

        if node_type == 'nCloth':
            mel.eval('nClothCreate;')
        elif node_type == 'nRigid':
            mel.eval('nClothMakeCollide;')
        elif node_type == 'hairSystem':
            mel.eval('assignNewHairSystem;')
        else:
            raise RuntimeError()

        _ = _attribute.NodeAttribute.get_target_nodes(
            target_shape_path, 'worldMesh', node_type
        )
        if _:
            node_path = _[0]
            return node_path

    @classmethod
    def find_any_from(cls, target_shape_path):
        # source
        _ = _attribute.NodeAttribute.get_source_node(
            target_shape_path, 'inMesh'
        )
        if _:
            node_path = _
            node_type = _node.Node.get_type(node_path)
            if node_type == 'nCloth':
                return node_path
        # target
        _ = _attribute.NodeAttribute.get_target_nodes(
            target_shape_path, 'worldMesh'
        )
        if _:
            node_path = _[0]
            node_type = _node.Node.get_type(node_path)
            if node_type == 'nRigid':
                return node_path


class NCloth:
    PRESET_KEY_INCLUDES = [
        'addCrossLinks',
        'airTightness',
        'bendAngleDropoff',
        'bendAngleScale',
        'bendMap',
        'bendMapType',
        'bendResistance',
        'bounce',
        'bounceMapType',
        'collide',
        'compressionResistance',
        'crossoverPush',
        'damp',
        'dampMapType',
        'deformMap',
        'deformMapType',
        'deformResistance',
        'drag',
        'evaluationOrder',
        'fieldDistance',
        'fieldMagnitude',
        'fieldMagnitudeMap',
        'fieldScale[0].fieldScale_FloatValue',
        'fieldScale[0].fieldScale_Interp',
        'fieldScale[0].fieldScale_Position',
        'fieldScale[1].fieldScale_FloatValue',
        'fieldScale[1].fieldScale_Interp',
        'fieldScale[1].fieldScale_Position',
        'forceField',
        'friction',
        'frictionMapType',
        'ignoreSolverGravity',
        'incompressibility',
        'inputAttractDamp',
        'inputAttractMap',
        'inputAttractMapType',
        'inputMeshAttract',
        'lift',
        'massMap',
        'massMapType',
        'pointFieldDistance',
        'pointFieldDropoff[0].pointFieldDropoff_FloatValue',
        'pointFieldDropoff[0].pointFieldDropoff_Interp',
        'pointFieldDropoff[0].pointFieldDropoff_Position',
        'pointFieldDropoff[1].pointFieldDropoff_FloatValue',
        'pointFieldDropoff[1].pointFieldDropoff_Interp',
        'pointFieldDropoff[1].pointFieldDropoff_Position',
        'pointFieldMagnitude',
        'pointForceField',
        'pointMass',
        'pressure',
        'pressureDamping',
        'pressureMethod',
        'pumpRate',
        'pushOut',
        'restLengthScale',
        'restitutionAngle',
        'restitutionTension',
        'rigidity',
        'rigidityMap',
        'rigidityMapType',
        'scalingRelation',
        'sealHoles',
        'selfAttract',
        'selfCollide',
        'selfCrossoverPush',
        'shearResistance',
        'solverDisplay',
        'sortLinks',
        'startPressure',
        'stretchDamp',
        'stretchMap',
        'stretchMapType',
        'stretchResistance',
        'tangentialDrag',
        'thicknessMapType',
        'trappedCheck',
        'wrinkleMap',
        'wrinkleMapScale',
        'wrinkleMapType'
    ]

    @classmethod
    def find_input_mesh_transform(cls, path):
        # target
        _ = _attribute.NodeAttribute.get_source_node(
            path, 'inputMesh', 'mesh'
        )
        if _:
            return _shape.Shape.get_transform(_)

    @classmethod
    def find_input_mesh_shape(cls, path):
        # target
        return _attribute.NodeAttribute.get_source_node(
            path, 'inputMesh', 'mesh'
        )

    @classmethod
    def find_output_mesh_shapes(cls, path):
        return _attribute.NodeAttribute.get_target_nodes(
            path, 'outputMesh', 'mesh'
        )

    @classmethod
    def get_nucleus(cls, shape_path):
        return _attribute.NodeAttribute.get_source_node(
            shape_path, 'startFrame', 'nucleus'
        )

    @classmethod
    def create_enable_aux(cls, path):
        name = path.split('|')[-1]
        input_cdt_name = '{}_input_cdt'.format(name)
        if cmds.objExists(input_cdt_name) is False:
            input_mesh_shape = cls.find_input_mesh_shape(path)
            if input_mesh_shape:
                cmds.createNode('condition', name=input_cdt_name, skipSelect=1)
                cmds.setAttr(input_cdt_name+'.secondTerm', 1)
                cmds.setAttr(input_cdt_name+'.operation', 1)
                cmds.connectAttr(
                    path+'.isDynamic', input_cdt_name+'.firstTerm'
                )
                cmds.connectAttr(
                    input_cdt_name+'.outColorR', input_mesh_shape+'.intermediateObject'
                )

        output_cdt_name = '{}_output_cdt'.format(name)
        if cmds.objExists(output_cdt_name) is False:
            output_mesh_shapes = cls.find_output_mesh_shapes(path)
            if output_mesh_shapes:
                output_mesh_shape = output_mesh_shapes[0]
                cmds.createNode('condition', name=output_cdt_name, skipSelect=1)
                cmds.setAttr(output_cdt_name+'.secondTerm', 1)
                cmds.setAttr(output_cdt_name+'.operation', 0)
                cmds.connectAttr(
                    path+'.isDynamic', output_cdt_name+'.firstTerm'
                )
                cmds.connectAttr(
                    output_cdt_name+'.outColorR', output_mesh_shape+'.intermediateObject'
                )


class MeshNCloth:
    @classmethod
    def get_args(cls, transform_path):
        shape = cls.get_nshape(transform_path)
        if shape:
            ntransform = _shape.Shape.get_transform(shape)
            nucleus = NCloth.get_nucleus(shape)
            return ntransform, nucleus

    @classmethod
    def get_nshape(cls, transform_path):
        shape_path = _node_for_transform.Transform.get_shape(transform_path)
        return _attribute.NodeAttribute.get_source_node(
            shape_path, 'inMesh', 'nCloth'
        )

    @classmethod
    def create_auto(cls, transform_path):
        args = cls.get_args(transform_path)
        if args:
            return False, args

        cmds.select(transform_path)
        mel.eval('nClothCreate;')
        return True, cls.get_args(transform_path)


class NRigid:
    @classmethod
    def find_input_mesh_transform(cls, path):
        # source
        _ = _attribute.NodeAttribute.get_source_node(
            path, 'inputMesh', 'mesh'
        )
        if _:
            return _shape.Shape.get_transform(_)

    @classmethod
    def get_nucleus(cls, shape_path):
        return _attribute.NodeAttribute.get_source_node(
            shape_path, 'startFrame', 'nucleus'
        )


class MeshNRigid:

    @classmethod
    def get_args(cls, transform_path):
        shape = cls.get_nshape(transform_path)
        if shape:
            ntransform = _shape.Shape.get_transform(shape)
            nucleus = NCloth.get_nucleus(shape)
            return ntransform, nucleus

    @classmethod
    def get_nshape(cls, transform_path):
        shape_path = _node_for_transform.Transform.get_shape(transform_path)
        _ = _attribute.NodeAttribute.get_target_nodes(
            shape_path, 'worldMesh[0]', 'nRigid'
        )
        if _:
            return _[0]

    @classmethod
    def create_auto(cls, transform_path):
        args = cls.get_args(transform_path)
        if args:
            return False, args

        cmds.select(transform_path)
        mel.eval('nClothMakeCollide;')
        return True, cls.get_args(transform_path)


class Field:
    @classmethod
    def create_for(cls, node_type, target_shape_path, target_any_paths):
        """
        Air;
        """
        target_any_paths = [
            _shape.Shape.get_transform(x) if _shape.Shape.check_is_shape(x) else x
            for x in target_any_paths
        ]
        cmds.select(target_any_paths)

        if _node_for_transform.Transform.is_transform_type(target_shape_path):
            target_shape_path = _node_for_transform.Transform.get_shape(target_shape_path)

        if node_type == 'airField':
            mel.eval('Air;')
        else:
            raise RuntimeError()


class MeshDynamic:
    @classmethod
    def is_valid(cls, transform_path):
        shape = _node_for_transform.Transform.get_shape(transform_path)
        history = cmds.listHistory(shape)
        _ = cmds.ls(history, type=['nCloth']) or []
        if _:
            return True
        return False


class Nucleus:
    LOG_KEY = 'nucleus'

    @classmethod
    def assign_to(cls, nucleus_path, shape_path, force=False):
        """
        assign auto, when force is False: node is connected to any nucleus, ignore
        """
        atr_names = [
            ('startState', 'inputPassiveStart'),
            ('currentState', 'inputPassive'),
        ]
        for i_name_src, i_name_tgt in atr_names:
            i_src = shape_path+'.'+i_name_src
            i_cs = cmds.listConnections(
                i_src, destination=1, source=0, plugs=1
            ) or []
            if i_cs:
                i_c = i_cs[0]
                i_node = i_c.split('.')[0]
                if cmds.nodeType(i_node) == 'nucleus':
                    if force is False:
                        continue

            j_tgt = None
            for j in range(100):
                j_tgt = nucleus_path+'.'+i_name_tgt+'[{}]'.format(j)
                j_cs = cmds.listConnections(
                    j_tgt, destination=0, source=1, plugs=1
                ) or []
                if not j_cs:
                    cmds.connectAttr(i_src, j_tgt, force=1)
                    break

            if j_tgt:
                bsc_log.Log.trace_method_result(
                    cls.LOG_KEY, 'repair solver connection: {} > {}'.format(
                        i_src, j_tgt
                    )
                )
