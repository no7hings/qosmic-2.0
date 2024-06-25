# coding:utf-8
import qsm_maya.core as qsm_mya_core

from . import base as _base


class NonLinearShapeOpt(_base.AbsShapeOpt):
    SCHEME_BASE = '/non_linear'

    TYPE_INCLUDES = [
        'deformBend',
        'deformFlare',
        'deformSine',
        'deformSquash',
        'deformTwist',
        'deformWave',
    ]

    TARGET_TYPE_INCLUDES = [
        'mesh'
    ]

    DATA_KEY_INCLUDES = [
        _base.Util.DataKeys.Node,
        _base.Util.DataKeys.Transform,
        _base.Util.DataKeys.Targets
    ]

    TARGET_ARGS = [
        ('deformerData', 'nonLinear')
    ]

    def __init__(self, *args, **kwargs):
        super(NonLinearShapeOpt, self).__init__(*args, **kwargs)


class NonlinearCreator(_base.AbsNodeCreator):
    KEY_MAPPER = dict(
        deformBend='bend',
        deformFlare='flare',
        deformSine='sine',
        deformSquash='squash',
        deformTwist='twist',
        deformWave='wave',
    )

    TARGET_TYPE_INCLUDES = [
        'mesh'
    ]

    def __init__(self, *args, **kwargs):
        super(NonlinearCreator, self).__init__(*args, **kwargs)

    @qsm_mya_core.Undo.execute
    def do_create(self):
        result = qsm_mya_core.NonLinear.create_for(
            self.KEY_MAPPER[self._node_type], self._target_node_path, self._target_any_paths
        )
        if result is not None:
            return NonLinearShapeOpt(
                result
            )


class NucleusShapeOpt(_base.AbsShapeOpt):
    SCHEME_BASE = '/nucleus'

    TYPE_INCLUDES = [
        'hairSystem',
        'nCloth',
        'nRigid',
        'nParticle',
    ]

    TARGET_TYPE_INCLUDES = [
        'mesh'
    ]

    DATA_KEY_INCLUDES = [
        _base.Util.DataKeys.Node,
        _base.Util.DataKeys.Transform,
        _base.Util.DataKeys.Targets
    ]

    SOURCE_ARGS = [
        ('nextState', 'nucleus')
    ]

    def __init__(self, *args, **kwargs):
        super(NucleusShapeOpt, self).__init__(*args, **kwargs)


class NucleusCreator(_base.AbsNodeCreator):
    TARGET_TYPE_INCLUDES = [
        'mesh'
    ]

    def __init__(self, *args, **kwargs):
        super(NucleusCreator, self).__init__(*args, **kwargs)

    @qsm_mya_core.Undo.execute
    def do_create(self):
        result = qsm_mya_core.RebuildForNucleus.create_for(
            self._node_type, self._target_node_path, self._target_any_paths
        )
        if result is not None:
            return NucleusShapeOpt(
                result
            )


class FieldOpt(_base.AbsNodeOpt):
    SCHEME_BASE = '/field'

    TYPE_INCLUDES = [
        'airField',
        'dragField',
        'gravityField',
        'newtonField',
        'radialField',
        'turbulenceField',
        'uniformField',
        'vortexField',
    ]

    DATA_KEY_INCLUDES = [
        _base.Util.DataKeys.Node,
    ]

    def __init__(self, *args, **kwargs):
        super(FieldOpt, self).__init__(*args, **kwargs)


class FieldCreator(_base.AbsNodeCreator):
    TARGET_TYPE_INCLUDES = [
        'nCloth',
    ]

    def __init__(self, *args, **kwargs):
        super(FieldCreator, self).__init__(*args, **kwargs)

    @qsm_mya_core.Undo.execute
    def do_create(self):
        result = qsm_mya_core.Field.create_for(
            self._node_type, self._target_node_path, self._target_any_paths
        )
        if result is not None:
            return FieldOpt(
                result
            )
