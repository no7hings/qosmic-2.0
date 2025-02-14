# coding:utf-8
from ... import abc_


class NCloth(abc_.AbsShapeOpt):
    SHAPE_TYPE = 'nCloth'

    DEFAULT_PROPERTIES = dict(
        displayColor=(1, 0, 1),

        inputMeshAttract=1,
        inputAttractMethod=1,
        inputAttractMapType=1
    )

    def __init__(self, *args, **kwargs):
        super(NCloth, self).__init__(*args, **kwargs)


class NRigid(abc_.AbsShapeOpt):
    SHAPE_TYPE = 'nRigid'

    DEFAULT_PROPERTIES = dict(
        displayColor=(0, 0, 1)
    )

    def __init__(self, *args, **kwargs):
        super(NRigid, self).__init__(*args, **kwargs)
