# coding:utf-8
import lxbasic.core as bsc_core

import lxgui.proxy.core as gui_prx_core

import lxtool.submitter.gui.widgets as smt_gui_widgets

bsc_core.EnvExtraMtd.set_td_enable(True)

# hook_option = 'file={}'.format('/l/prod/cgm/work/shots/z88/z88070/ani/animation/maya/scenes/z88070.ani.animation.v026.ma')
hook_option = 'file={}'.format('/l/prod/xkt/work/shots/z88/z88010/efx/effects/houdini/z88010.efx.effects.v032.hip')
# hook_option = 'file={}'.format('/l/prod/xkt/work/shots/z88/z88100/cfx/hair/houdini/z88100.cfx.hair.v010.hip')

gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
    smt_gui_widgets.PnlSubmitterForShotRender, hook_option=hook_option
)
