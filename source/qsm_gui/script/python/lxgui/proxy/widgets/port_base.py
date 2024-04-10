# coding:utf-8
# qt widgets
from ...qt.widgets import utility as gui_qt_wgt_utility

from ...qt.widgets import button as gui_qt_wgt_button

from ...qt.widgets import item as gui_qt_wgt_item
# proxy abstracts
from .. import abstracts as gui_prx_abstracts


class AttrConfig(object):
    PRX_PORT_HEIGHT = 24
    PRX_PORT_HEIGHT_2 = 82


# port
#   info
class PrxPortInfo(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_button.QtIconPressButton

    def __init__(self, *args, **kwargs):
        super(PrxPortInfo, self).__init__(*args, **kwargs)
        # self.widget.setAlignment(gui_qt_core.QtCore.Qt.AlignRight | gui_qt_core.QtCore.Qt.AlignVCenter)
        self.widget.setMaximumHeight(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMinimumHeight(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMaximumWidth(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMinimumWidth(AttrConfig.PRX_PORT_HEIGHT)

    def set(self, boolean):
        self.widget._set_checked_(boolean)


#   status
class PrxPortStatus(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_item._QtStatusItem

    def __init__(self, *args, **kwargs):
        super(PrxPortStatus, self).__init__(*args, **kwargs)
        # self.widget.setAlignment(gui_qt_core.QtCore.Qt.AlignRight | gui_qt_core.QtCore.Qt.AlignVCenter)
        self.widget.setMaximumHeight(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMinimumHeight(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMaximumWidth(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMinimumWidth(AttrConfig.PRX_PORT_HEIGHT)
        self.widget._set_tool_tip_text_(
            '"LMB-click" to use value "default" / "local" / "global"'
        )

    def set(self, boolean):
        self.widget._set_checked_(boolean)


#   label
class PrxPortLabel(gui_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = gui_qt_wgt_utility.QtTextItem

    def __init__(self, *args, **kwargs):
        super(PrxPortLabel, self).__init__(*args, **kwargs)
        # self.widget.setAlignment(gui_qt_core.QtCore.Qt.AlignRight | gui_qt_core.QtCore.Qt.AlignVCenter)
        self.widget.setMaximumHeight(AttrConfig.PRX_PORT_HEIGHT)
        self.widget.setMinimumHeight(AttrConfig.PRX_PORT_HEIGHT)
        # self._qt_widget._set_name_align_(gui_configure.AlignRegion.Top)

    def set_name(self, text):
        self._qt_widget._set_name_text_(text)

    def set_width(self, w):
        self.widget.setMaximumWidth(w)
        self.widget.setMinimumWidth(w)

    def set_info_tool_tip(self, text):
        pass

    def set_name_tool_tip(self, *args, **kwargs):
        if hasattr(self._qt_widget, '_set_tool_tip_'):
            self._qt_widget._set_tool_tip_(args[0], **kwargs)

    def get_name_draw_width(self):
        return self._qt_widget._get_name_text_draw_width_()
