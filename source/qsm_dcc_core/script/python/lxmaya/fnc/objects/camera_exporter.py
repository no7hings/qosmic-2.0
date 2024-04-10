# coding:utf-8
import collections

import lxcontent.core as ctt_core

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.fnc.abstracts as bsc_fnc_abstracts
# maya
from ...core.wrap import *

from ... import core as mya_core
# maya dcc
from ...dcc import objects as mya_dcc_objects


class FncExporterForCameraYml(
    bsc_fnc_abstracts.AbsFncOptionBase
):
    OPTION = dict(
        file='',
        root=''
    )

    def __init__(self, option):
        super(FncExporterForCameraYml, self).__init__(option)
        #
        self._raw = ctt_core.Content(
            value=collections.OrderedDict()
        )

    @classmethod
    def _set_camera_create_(cls, root, persp_view):
        dcc_root_dag_path = bsc_core.PthNodeOpt(root)
        mya_root_dag_path = dcc_root_dag_path.translate_to(
            pathsep='|'
        )
        mya_camera = mya_dcc_objects.Shape('|persp_view')
        mya_camera = mya_camera.set_create('camera')
        camera_transform = mya_camera.transform.path
        camera_shape = mya_camera.path
        #
        cmds.camera(
            camera_shape,
            edit=1,
            displayFilmGate=0,
            displaySafeAction=0,
            displaySafeTitle=0,
            displayFieldChart=0,
            displayResolution=1,
            displayGateMask=1,
            filmFit=1,
            focalLength=35.000,
            overscan=1.0,
            nearClipPlane=0.1,
            farClipPlane=1000000.0
        )
        #
        if persp_view is True:
            cmds.camera(
                camera_shape,
                edit=1,
                position=(28.0, 21.0, 28.0),
                rotation=(-27.9383527296, 45, 0)
            )
        #
        cmds.setAttr(camera_shape+'.displayGateMaskOpacity', 1)
        cmds.setAttr(camera_shape+'.displayGateMaskColor', 0, 0, 0, type='double3')
        #
        cmds.viewFit(
            camera_shape,
            [mya_root_dag_path.value],
            fitFactor=1.0,
            animate=0
        )
        cmds.camera(
            camera_shape,
            edit=1,
            focalLength=67.177,
        )
        return camera_transform, camera_shape

    @mya_core.MyaModifier.undo_debug_run
    def set_run(self):
        file_path = self._option['file']
        root = self._option['root']
        camera_transform, camera_shape = self._set_camera_create_(root, persp_view=True)
        #
        for p in mya_core.CmdObjOpt(camera_transform).get_ports(includes=['translate', 'rotate', 'scale']):
            self._raw.set(
                'persp.transform.{}'.format(p.get_port_path()), p.get()
            )
        #
        for p in mya_core.CmdObjOpt(camera_shape).get_ports(includes=['focalLength', 'farClipPlane', 'nearClipPlane']):
            self._raw.set(
                'persp.shape.{}'.format(p.get_port_path()), p.get()
            )
        #
        self._raw.save_to(file_path)
        bsc_log.Log.trace_method_result(
            'camera-yml-export',
            'file="{}"'.format(file_path)
        )
        cmds.delete(camera_transform)
