# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import qsm_lazy_montage.core as qsm_lzy_mtg_core


class AbsMontage(object):
    ROOT_PATH = '|__MONTAGE__'

    class AtrKeys:
        Root = [
            'translateX', 'translateY', 'translateZ',
            'rotateX', 'rotateY', 'rotateZ'
        ]
        Default = [
            'rotateX', 'rotateY', 'rotateZ'
        ]

    class Namespaces:
        Transfer = 'transfer'

    DEFAULT_MASTER_LOWER_HEIGHT = 8.36773617093
    DEFAULT_MASTER_HEIGHT = 15.2693830421
    DEFAULT_MASTER_UPPER_HEIGHT = 6.83376148885

    DEBUG_MODE = True

    def __init__(self):
        self._configure = qsm_lzy_mtg_core.MtgConfigure()

    @classmethod
    def create_root(cls):
        if cmds.objExists(cls.ROOT_PATH) is False:
            name = cls.ROOT_PATH.split('|')[-1]
            cmds.createNode(
                'dagContainer', name=name, shared=1, skipSelect=1
            )
            cmds.setAttr(
                cls.ROOT_PATH+'.iconName', 'folder-closed.png', type='string'
            )
        return cls.ROOT_PATH
