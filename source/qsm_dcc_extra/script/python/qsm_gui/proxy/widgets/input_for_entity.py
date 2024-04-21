# coding:utf-8
import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.abstracts as prx_abstracts

import qsm_general.entity as qsm_gnl_entity


class PrxInputForAsset(prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = qt_widgets.QtTranslucentWidget

    def __init__(self, *args, **kwargs):
        super(PrxInputForAsset, self).__init__(*args, **kwargs)

        l_0 = qt_widgets.QtHBoxLayout(self.get_widget())
        l_0.setContentsMargins(*[0]*4)
        # l_0._set_align_as_top_()
        self._qt_path_input = qt_widgets.QtInputAsPath()
        l_0.addWidget(self._qt_path_input)

        self._entity_root = qsm_gnl_entity.Root()

        self._qt_path_input._set_buffer_fnc_(
            self._buffer_fnc
        )

        self._qt_path_input._set_value_('/')
        self._qt_path_input._set_choose_popup_auto_resize_enable_(False)
        self._qt_path_input._set_choose_popup_tag_filter_enable_(True)
        self._qt_path_input._set_choose_popup_keyword_filter_enable_(True)

        self._qt_path_input._set_choose_popup_item_size_(40, 40)

        self._qt_path_input._setup_()

        self._qt_button = qt_widgets.QtPressButton()
        l_0.addWidget(self._qt_button)
        self._qt_button._set_name_text_('reference')
        self._qt_button.setMaximumWidth(64)
        self._qt_button.setMinimumWidth(64)

    def _buffer_fnc(self, path):
        cs = path.get_components()
        cs.reverse()
        d = len(cs)
        if d == 1:
            names = [i.name for i in self._entity_root.projects]
            return dict(
                names=names
            )
        elif d == 2:
            entity = self._entity_root.find_entity(path.to_string())
            if entity is not None:
                names = [i.name for i in entity.assets]
                return dict(
                    names=names
                )
        return dict()
