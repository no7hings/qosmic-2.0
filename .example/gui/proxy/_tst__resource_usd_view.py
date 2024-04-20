# coding:utf-8
import lxresource as bsc_resource

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.proxy.widgets as prx_widgets

import lxgui.proxy.core as gui_prx_core

import lxbasic.database as bsc_database

import lxbasic.dcc.core as bsc_dcc_core

bsc_log.Log.TEST = True


class W(prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(W, self).__init__(*args, **kwargs)
        img_w, img_h = 515, 515
        self.set_definition_window_size([img_w+36, img_h+54])

        s = prx_widgets.PrxHSplitter()
        self.add_widget(s)

        self._usd_stage_view = prx_widgets.PrxUsdStageView()
        s.add_widget(self._usd_stage_view)
        # self._data = [
        #     # '/3d_plant_proxy/tree_a001_rsc',
        #     # '/3d_plant_proxy/tree_a002_rsc',
        #     # #
        #     # '/3d_plant_proxy/tree_b001_rsc',
        #     # '/3d_plant_proxy/tree_b002_rsc',
        #     # #
        #     # '/3d_plant_proxy/tree_c001_rsc',
        #     # '/3d_plant_proxy/tree_c002_rsc',
        #     # #
        #     # '/3d_plant_proxy/tree_d001_rsc',
        #     # '/3d_plant_proxy/tree_d002_rsc',
        #     # #
        #     # '/3d_plant_proxy/tree_e001_rsc',
        #     # '/3d_plant_proxy/tree_e002_rsc',
        #
        #     # '/3d_plant_proxy/tree_f001_rsc',
        #     # '/3d_plant_proxy/tree_g001_rsc',
        #     # '/3d_plant_proxy/tree_h001_rsc',
        #     # '/3d_plant_proxy/tree_i001_rsc',
        #     # '/3d_plant_proxy/tree_j001_rsc',
        #     # '/3d_plant_proxy/tree_k001_rsc',
        #
        #     # '/3d_plant_proxy/tree_f002_rsc',
        #     # '/3d_plant_proxy/tree_g002_rsc',
        #     # '/3d_plant_proxy/tree_h002_rsc',
        #     # '/3d_plant_proxy/tree_i002_rsc',
        #     '/3d_plant_proxy/tree_j002_rsc',
        #
        #     '/3d_plant_proxy/tree_k002_rsc',
        # ]

        self.build_lib_resource('/3d_plant_proxy/grass_a001_rsc')

    def build_lib_resource(self, resource_path):
        def cache_fnc_():
            bsc_log.Log.test_start('build stage')
            self._usd_stage_view.refresh_usd_stage_for_asset_preview(
                usd_file=dtb_version_opt.get_geometry_usd_file(force=True),
                look_preview_usd_file=dtb_version_opt.get_look_preview_usd_file(),
            )
            bsc_log.Log.test_end('build stage')
            return []

        def build_fnc_():
            bsc_log.Log.test_start('refresh stage')
            self._usd_stage_view.refresh_usd_view_draw()
            bsc_log.Log.test_end('refresh stage')
            self._usd_stage_view.widget._usd_switch_camera_to_('/cameras/cam_front/cam_front_shape')

        def post_fnc_():
            pass

        version_path = '{}/v0001'.format(resource_path)
        path_opt = bsc_core.PthNodeOpt(version_path)
        cs = path_opt.get_components()
        category_group = cs[-2].get_name()
        dtb_opt = bsc_database.DtbOptForResource(
            bsc_resource.RscExtendConfigure.get_yaml('database/library/resource-basic'),
            bsc_resource.RscExtendConfigure.get_yaml('database/library/resource-{}'.format(category_group))
        )
        dtb_version = dtb_opt.get_dtb_version(version_path)

        dtb_version_opt = bsc_database.DtbNodeOptForRscVersion(
            dtb_opt, dtb_version
        )

        self._usd_stage_view.run_as_thread(
            cache_fnc_, build_fnc_, post_fnc_
        )


if __name__ == '__main__':

    bsc_dcc_core.OcioSetup(
        bsc_storage.StgPathMapper.map_to_current(
            '/job/PLE/bundle/thirdparty/aces/1.2'
        )
    ).set_run()

    w = gui_prx_core.GuiProxyUtil.show_window_proxy_auto(W)


