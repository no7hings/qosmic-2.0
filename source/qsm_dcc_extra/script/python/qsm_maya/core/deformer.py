# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.internal.common.cmd.base as cmd_base

from . import attribute as _attribute

from . import transform as _transform


class NonLinear(object):
    @classmethod
    def create_for(cls, key, shape, components):
        cmds.select(components)

        if _transform.Transform.is_transform(shape):
            shape = _transform.Transform.get_shape(shape)

        cmd_base.executeCommand('{}.cmd_create'.format(key))
        node = _attribute.NodeAttribute.get_source_node(
            shape, 'inMesh', 'nonLinear'
        )
        handle_shape = _attribute.NodeAttribute.get_source_node(
            node, 'deformerData', 'deform'+key.capitalize()
        )
        return handle_shape

    @classmethod
    def create_bend_for(cls, shape, components):
        return cls.create_for('bend', shape, components)

    @classmethod
    def create_flare_for(cls, shape, components):
        return cls.create_for('flare', shape, components)

    @classmethod
    def create_sine_for(cls, shape, components):
        return cls.create_for('sine', shape, components)

    @classmethod
    def create_squash_for(cls, shape, components):
        return cls.create_for('squash', shape, components)

    @classmethod
    def create_twist_for(cls, shape, components):
        return cls.create_for('twist', shape, components)

    @classmethod
    def create_wave_for(cls, shape, components):
        return cls.create_for('wave', shape, components)

