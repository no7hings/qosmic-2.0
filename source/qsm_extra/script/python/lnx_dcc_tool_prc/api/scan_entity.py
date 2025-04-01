# coding:utf-8
from ..gui.proxy import widgets as _gui_prx_widgets


def get_asset_entity():
    wgt = _gui_prx_widgets.PrxWindowForAssetInput()
    wgt.show_window_auto(size=(480, 96))

    if wgt.get_result() is True:
        return wgt.get_entity()
