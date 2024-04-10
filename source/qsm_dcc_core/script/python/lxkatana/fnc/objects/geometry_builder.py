# coding:utf-8
import types

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.fnc.abstracts as bsc_fnc_abstracts

import lxresolver.core as rsv_core
# katana
# katana dcc
from ...dcc import objects as ktn_dcc_objects


# todo: old method need remove
class FncBuilderForAssetOld(bsc_fnc_abstracts.AbsFncOptionBase):
    VAR_NAMES = ['hi', 'lo', 'shape']
    #
    OPTION = dict(
        project='',
        asset='',
        #
        with_camera=False,
        camera_option='step=srf&task=surfacing&version=latest',
        #
        geometry_var_names=VAR_NAMES
    )

    def __init__(self, option=None):
        super(FncBuilderForAssetOld, self).__init__(option)

    @classmethod
    def _set_camera_build_(cls, option):
        option_opt = bsc_core.ArgDictStringOpt(option)
        rsv_task = rsv_core.RsvBase.generate_root().get_rsv_task(**option_opt.value)
        version = option_opt.get('version')
        cls._set_camera_build_by_abc_(rsv_task, version)

    @classmethod
    def _set_camera_build_by_abc_(cls, rsv_task, version):
        camera_abc_file_unit = rsv_task.get_rsv_unit(
            keyword='asset-camera-persp-abc-file'
        )
        camera_abc_file_path = camera_abc_file_unit.get_result(version=version)
        if camera_abc_file_path is not None:
            ktn_workspace = ktn_dcc_objects.AssetWorkspaceOld()
            #
            ktn_workspace.set_camera_persp_abc_import(
                camera_abc_file_path,
                '/cameras/camera_locator/persp_view/persp_viewShape'
            )
            ktn_workspace.set_render_camera(
                '/cameras/camera_locator/persp_view/persp_viewShape'
            )

    def set_run(self):
        project = self._option['project']
        asset = self._option['asset']
        #
        with_camera = self._option['with_camera']
        camera_option = self._option['camera_option']
        #
        method_args = [
            (with_camera, self._set_camera_build_, camera_option)
        ]
        #
        if method_args:
            g_p = bsc_log.LogProcessContext(maximum=len(method_args))
            for i_enable, i_method, i_option in method_args:
                g_p.do_update()
                #
                if isinstance(i_method, types.MethodType):
                    i_option += '&project={}&asset={}'.format(project, asset)
                    i_method(i_option)
            #
            g_p.set_stop()
