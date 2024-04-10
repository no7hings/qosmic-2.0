# coding:utf-8
import six
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.log as bsc_log
# maya
from ... import core as mya_core

from ... import abstracts as mya_abstracts

from . import utility as mya_dcc_obj_utility

from . import node as mya_dcc_obj_node


class Group(mya_dcc_obj_node.Node):
    def __init__(self, path):
        super(Group, self).__init__(path)

    def get_all_shape_paths(self, include_obj_type=None):
        if include_obj_type is not None:
            if isinstance(include_obj_type, six.string_types):
                _ = [include_obj_type]
            elif isinstance(include_obj_type, (tuple, list)):
                _ = include_obj_type
            else:
                raise TypeError()
            return cmds.ls(self.path, noIntermediate=1, dagObjects=1, type=_, long=1) or []
        return cmds.ls(self.path, shapes=1, noIntermediate=1, dagObjects=1, long=1) or []

    def get_all_paths(self, include_obj_type=None):
        if include_obj_type is not None:
            if isinstance(include_obj_type, six.string_types):
                _ = [include_obj_type]
            elif isinstance(include_obj_type, (tuple, list)):
                _ = include_obj_type
            else:
                raise TypeError()
            return cmds.ls(self.path, noIntermediate=1, dagObjects=1, type=_, long=1) or []
        return cmds.ls(self.path, noIntermediate=1, dagObjects=1, long=1) or []

    def create_child(self, name):
        child_path = self.PATHSEP.join([self.get_path(), name])
        if cmds.objExists(child_path) is False:
            cmds.group(empty=1, name=name, parent=self.get_path())
        return self.__class__(child_path)


class Transform(mya_dcc_obj_node.Node):
    DEFAULT_MATRIX = [
        1.0, .0, .0, .0,
        .0, 1.0, .0, .0,
        .0, .0, 1.0, .0,
        .0, .0, .0, 1.0
    ]
    DEFAULT_TRANSFORMATION = [
        (0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0),
        (1.0, 1.0, 1.0)
    ]

    def __init__(self, path):
        super(Transform, self).__init__(path)

    def get_visible(self):
        return self.get_port('visibility').get()

    def set_visible(self, boolean):
        self.get_port('visibility').set(boolean)

    def get_matrix(self):
        return cmds.xform(
            self.path,
            query=1,
            matrix=1,
            worldSpace=1
        )

    def get_matrix_is_changed(self):
        return self.get_matrix() != self.DEFAULT_MATRIX

    def set_matrix(self, matrix):
        cmds.xform(self.path, matrix=matrix, worldSpace=1)

    def get_transformations(self, round_count=4):
        lis = []
        port_names = [
            'translate', 'rotate', 'scale'
        ]
        for port_name in port_names:
            atr_path = '{}.{}'.format(self.path, port_name)
            data = cmds.getAttr(atr_path)
            lis.append(
                tuple([round(i, round_count) for i in data[0]])
            )
        return lis

    def set_transformations(self, transformations):
        port_names = [
            ('tx', 'ty', 'tz'),
            ('rx', 'ry', 'rz'),
            ('sx', 'sy', 'sz'),
            # ('prx', 'pry', 'prz'),
            # ('px', 'py', 'pz'),
        ]
        for a, channel_names in enumerate(port_names):
            for b, channel_name in enumerate(channel_names):
                port = self.get_port(channel_name)
                port.set(transformations[a][b])


class Shape(
    mya_abstracts.AbsMyaNode,
    mya_abstracts.AbsMyaShapeDef
):
    DCC_PORT_CLS = mya_dcc_obj_utility.Port
    TRANSFORM_CLS = Transform

    def __init__(self, path):
        if cmds.objExists(path) is True:
            if cmds.nodeType(path) == mya_core.MyaNodeTypes.Transform:
                _ = cmds.listRelatives(path, children=1, shapes=1, noIntermediate=1, fullPath=1)
                if _:
                    shape_path = _[0]
                else:
                    raise TypeError()
            else:
                shape_path = cmds.ls(path, long=1)[0]
        else:
            shape_path = path
        super(Shape, self).__init__(shape_path)
        self._set_ma_shape_def_init_(self.path)

    def get_is_visible(self):
        pass

    def set_create(self, obj_type):
        if self.get_is_exists() is False:
            name = self.name
            shape_name = '{}Shape'.format(name)
            transform = cmds.createNode(obj_type, name=shape_name, skipSelect=1)
            bsc_log.Log.trace_method_result(
                'shape create',
                'obj="{}"'.format(self.path)
            )
            return self.__class__(transform)


class Camera(Shape):
    def __init__(self, path):
        super(Camera, self).__init__(path)

    def get_is_renderable(self):
        return self.get_port('renderable').get()

    def set_display_(self):
        cmds.camera(
            self.path,
            edit=1,
            displayFilmGate=0,
            displaySafeAction=0,
            displaySafeTitle=0,
            displayFieldChart=0,
            displayResolution=1,
            displayGateMask=1,
            #
            overscan=1.0,
            #
            nearClipPlane=0.01,
            farClipPlane=1000000.0,
        )
        cmds.setAttr(
            self.path+'.displayGateMaskOpacity', 1
        )
        cmds.setAttr(
            self.path+'.displayGateMaskColor', 0, 0, 0, type='double3'
        )

    def set_frame_to(self, location, percent=1.0):
        cmds.viewFit(
            self.path,
            [location],
            fitFactor=percent,
            animate=0
        )
        bsc_log.Log.trace_method_result(
            'camera frame to',
            'camera="{}", obj="{}"'.format(self.path, location)
        )


class Light(Shape):
    DCC_PORT_CLS = mya_dcc_obj_utility.Port
    DCC_CONNECTION_CLS = mya_dcc_obj_utility.Connection

    def __init__(self, path):
        super(Light, self).__init__(path)

    def set_create(self, obj_type):
        if self.get_is_exists() is False:
            name = self.name
            shape_name = '{}Shape'.format(name)
            transform = cmds.shadingNode(obj_type, name=shape_name, asLight=True)
            bsc_log.Log.trace_method_result(
                'light create',
                u'obj="{}"'.format(self.path)
            )
            return self.__class__(transform)
