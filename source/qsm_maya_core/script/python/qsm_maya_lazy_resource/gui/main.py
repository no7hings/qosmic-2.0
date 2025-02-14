# coding:utf-8
import qsm_lazy_resource.gui.abstracts as _abstracts

from qsm_lazy_resource.gui.pages import manager as _page_manager

from qsm_lazy_resource.gui.subpanels import register as _subpanel_register


class PrxLazyResourceTool(_abstracts.AbsPrxResourceTool):
    PAGE_CLASS_DICT = dict(
        manager=_page_manager.PrxPageForResourceManager
    )

    SUB_PANEL_CLASS_DICT = dict(
        register=_subpanel_register.PrxSubPanelForRegister
    )

    KEY_TAB_KEYS = 'lazy-resource-manager.page_keys_maya'
    HST_TAB_KEY_CURRENT = 'lazy-resource-manager.page_key_current_maya'

    def __init__(self, window, session, *args, **kwargs):
        super(PrxLazyResourceTool, self).__init__(window, session, *args, **kwargs)
