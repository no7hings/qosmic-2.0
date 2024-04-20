# coding:utf-8
import lxusd.startup as usd_startup

# usd_startup.UsdSetup(
#     '/data/e/myworkspace/td/lynxi/workspace/resource/linux/usd'
# ).set_run()

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.dcc.core as bsc_dcc_core

import lxgui.proxy.widgets as prx_widgets

import lxgui.proxy.core as gui_prx_core

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

        self._usd_stage_view.load_usd_file(
            '/production/shows/nsa_dev/assets/chr/td_test/shared/mod/modeling/td_test.mod.modeling.v031/cache/usd/td_test.usda'
        )
        self._usd_stage_view.refresh_usd_view_draw()
        self._usd_stage_view.get_usd_model().set_camera_light_enable(True)


if __name__ == '__main__':
    bsc_dcc_core.OcioSetup(
        bsc_storage.StgPathMapper.map_to_current(
            '/job/PLE/bundle/thirdparty/aces/1.2'
        )
    ).set_run()

    gui_prx_core.GuiProxyUtil.show_window_proxy_auto(W)
