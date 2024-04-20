# coding:utf-8
import lxbasic.core as bsc_core

import lxgui.proxy.core as gui_prx_core

import lxtool.submitter.gui.widgets as smt_gui_widgets

bsc_core.EnvExtraMtd.set_td_enable(True)

# hook_option = 'file={}'.format('/l/prod/cgm/work/assets/chr/nn_14y_test/mod/modeling/maya/scenes/nn_14y_test.mod.modeling.v006.ma')
# hook_option = 'file={}'.format('/l/prod/cgm/work/assets/chr/nn_14y_test/srf/surfacing/katana/nn_14y_test.srf.surfacing.v045.td_render.katana')
hook_option = 'file={}'.format('/l/prod/cgm/work/assets/chr/nn_4y_test/srf/surfacing/katana/nn_4y_test.srf.surfacing.v111.katana')
# hook_option = 'file={}'.format('/l/prod/cgm/work/assets/chr/nn_4y_test/mod/modeling/maya/scenes/nn_4y_test.mod.modeling.v053.ma')
# hook_option = 'file={}'.format('/l/prod/cgm/work/assets/chr/nn_4y_test/mod/modeling/maya/scenes/nn_4y_test.mod.modeling.v066.td.ma')
# hook_option = 'file={}'.format('/l/prod/cgm/work/assets/chr/nn_14y/mod/modeling/maya/scenes/nn_14y.mod.modeling.v013.ma')
# hook_option = 'file={}'.format('/l/prod/cgm/work/assets/chr/nn_4y_test/rig/rigging/maya/scenes/nn_4y_test.rig.rigging.v111.ma')
# hook_option = 'file={}'.format('/l/prod/cgm/work/assets/chr/nn_4y_test/grm/groom/maya/scenes/nn_4y_test.grm.groom.v103.ma')

gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    smt_gui_widgets.PnlSubmitterForAssetRender, hook_option=hook_option
)
