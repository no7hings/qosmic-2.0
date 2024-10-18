# coding:utf-8
import lxbasic.resource as bsc_resource

from ... import core as gui_core
# qt
from ...qt import core as gui_qt_core
# qt widgets
from ...qt.widgets import base as _qt_wgt_base

from ...qt.widgets import utility as _qt_wgt_utility
# proxy abstracts
from .. import abstracts as _prx_abstracts
# proxy widgets
from . import window_base as _window_base


class PrxBasePanel(_window_base.PrxBaseWindow):
    CONFIGURE_KEY = None

    PAGE_CLASS_DICT = {}
    SUB_PANEL_CLASS_DICT = {}
    SUB_PAGE_CLASS_DICT = {}

    def __init__(self, window, session, *args, **kwargs):
        super(PrxBasePanel, self).__init__(*args, **kwargs)
        self._init_base_panel_def(window, session, *args, **kwargs)

    def _gui_debug_run(self, fnc, *args, **kwargs):
        # noinspection PyBroadException
        try:
            fnc(*args, **kwargs)
        except Exception:
            import sys

            import traceback

            exc_texts = []
            exc_type, exc_value, exc_stack = sys.exc_info()
            if exc_type:
                value = '{}: "{}"'.format(exc_type.__name__, repr(exc_value))
                for seq, stk in enumerate(traceback.extract_tb(exc_stack)):
                    i_file_path, i_line, i_fnc, i_fnc_line = stk
                    exc_texts.append(
                        '{indent}file "{file}" line {line} in {fnc}\n{indent}{indent}{fnc_line}'.format(
                            **dict(
                                indent='    ',
                                file=i_file_path,
                                line=i_line,
                                fnc=i_fnc,
                                fnc_line=i_fnc_line
                            )
                        )
                    )
                #
                self.show_exception()
                self.set_exception_content_add('traceback:')
                [self.set_exception_content_add(i) for i in exc_texts]
                self.set_exception_content_add(value)

    def _gui_setup_fnc(self):
        self.gui_setup_fnc()

    def _init_base_panel_def(self, window, session, *args, **kwargs):
        if window is None:
            self._window = self
        else:
            self._window = window

        self._session = session

        self._language = gui_core.GuiUtil.get_language()

        self._gui_debug_run(
            self._gui_main_fnc, self.CONFIGURE_KEY
        )

    def _gui_main_fnc(self, configure_key):
        self._configure = bsc_resource.RscExtendConfigure.get_as_content(configure_key)
        self._option_configure = self._configure.get_as_content('option')
        self._gui_configure = self._configure.get_as_content('option.gui')

        self.set_window_title(
            gui_core.GuiUtil.choice_name(self._language, self._configure.get('option.gui'))
        )
        self.set_window_icon_by_name(
            self._configure.get('option.gui.icon_name')
        )
        self.set_definition_window_size(
            self._configure.get('option.gui.size')
        )

        self.register_window_close_method(self.gui_close_fnc)

        self.start_window_loading(
            self._gui_setup_fnc, post_fnc=self.gui_setup_post_fnc
        )

    def gui_close_fnc(self):
        pass

    def gui_setup_fnc(self):
        raise NotImplementedError()

    def gui_setup_post_fnc(self):
        pass

    def generate_sub_panel_for(self, key):
        return self.SUB_PANEL_CLASS_DICT[key](self._window, self._session)

    def generate_page_for(self, key):
        return self.PAGE_CLASS_DICT[key](self._window, self._session)

    def generate_sub_page_for(self, key, sub_window):
        return self.SUB_PAGE_CLASS_DICT[key](self._window, self._session, sub_window)


class PrxBasePage(_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget

    PAGE_KEY = None

    UNIT_CLASS_DICT = {}
    UNIT_CLASSES = []

    def __init__(self, window, session, *args, **kwargs):
        super(PrxBasePage, self).__init__(*args, **kwargs)

        self._window = window
        self._session = session

        self._qt_layout = _qt_wgt_base.QtVBoxLayout(self._qt_widget)
        self._qt_layout.setContentsMargins(*[0]*4)
        self._qt_layout.setSpacing(2)

    def gui_page_setup_fnc(self):
        """
        main setup function put here
        """

    def gui_page_setup_post_fnc(self):
        """
        fix some size bug for size setup delay
        """

    def generate_unit_for(self, key):
        return self.UNIT_CLASS_DICT[key](self._window, self, self._session)

    def _to_unit_instance(self, cls):
        return cls(self._window, self, self._session)


class PrxBaseUnit(_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget

    UNIT_KEY = None

    def __init__(self, window, page, session, *args, **kwargs):
        super(PrxBaseUnit, self).__init__(*args, **kwargs)

        self._window = window
        self._page = page
        self._session = session

        self._qt_layout = _qt_wgt_base.QtVBoxLayout(self._qt_widget)
        self._qt_layout.setContentsMargins(*[0]*4)
        self._qt_layout.setSpacing(2)

    def gui_unit_setup_fnc(self):
        pass


class PrxVirtualUnit(object):
    UNIT_KEY = None

    def __init__(self, window, page, session):
        self._window = window
        self._page = page
        self._session = session


class PrxBaseSubPanel(_window_base.PrxBaseWindow):
    CONFIGURE_KEY = None

    SUB_PANEL_KEY = None

    SUB_PAGE_CLASS_DICT = {}

    def __init__(self, window, session, *args, **kwargs):
        super(PrxBaseSubPanel, self).__init__(*args, **kwargs)
        self._init_base_panel_def(window, session, *args, **kwargs)

        self._page_dict = {}

    def _gui_debug_run(self, fnc, *args, **kwargs):
        # noinspection PyBroadException
        try:
            fnc(*args, **kwargs)
        except Exception:
            import sys

            import traceback

            exc_texts = []
            exc_type, exc_value, exc_stack = sys.exc_info()
            if exc_type:
                value = '{}: "{}"'.format(exc_type.__name__, repr(exc_value))
                for seq, stk in enumerate(traceback.extract_tb(exc_stack)):
                    i_file_path, i_line, i_fnc, i_fnc_line = stk
                    exc_texts.append(
                        '{indent}file "{file}" line {line} in {fnc}\n{indent}{indent}{fnc_line}'.format(
                            **dict(
                                indent='    ',
                                file=i_file_path,
                                line=i_line,
                                fnc=i_fnc,
                                fnc_line=i_fnc_line
                            )
                        )
                    )
                #
                self.show_exception()
                self.set_exception_content_add('traceback:')
                [self.set_exception_content_add(i) for i in exc_texts]
                self.set_exception_content_add(value)

    def _gui_setup_fnc(self):
        self.gui_setup_fnc()

    def _init_base_panel_def(self, window, session, *args, **kwargs):
        self._window = window
        if self._window is not None:
            self._qt_widget.setWindowFlags(gui_qt_core.QtCore.Qt.Tool)

        self._session = session

        self._sub_window = self

        self._language = gui_core.GuiUtil.get_language()

        self._gui_debug_run(
            self._gui_main_fnc, self.CONFIGURE_KEY
        )

    def _gui_main_fnc(self, configure_key):
        self._configure = bsc_resource.RscExtendConfigure.get_as_content(configure_key)
        self._option_configure = self._configure.get_as_content('option')
        self._gui_configure = self._configure.get_as_content('option.gui')

        self.set_window_title(
            gui_core.GuiUtil.choice_name(self._language, self._configure.get('option.gui'))
        )
        self.set_window_icon_by_name(
            self._configure.get('option.gui.icon_name')
        )
        self.set_definition_window_size(
            self._configure.get('option.gui.size')
        )

        self.register_window_close_method(self.gui_close_fnc)

        self._gui_setup_fnc()

    def gui_close_fnc(self):
        pass

    def gui_setup_fnc(self):
        pass

    def generate_sub_page_for(self, key):
        return self.SUB_PAGE_CLASS_DICT[key](self._window, self._session, self)

    def gui_get_page(self, key):
        return self._page_dict.get(key)


class PrxBaseSubPage(_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget

    PAGE_KEY = None

    def __init__(self, window, session, sub_window, *args, **kwargs):
        super(PrxBaseSubPage, self).__init__(*args, **kwargs)

        self._window = window
        self._session = session
        self._sub_window = sub_window

        self._qt_layout = _qt_wgt_base.QtVBoxLayout(self._qt_widget)
        self._qt_layout.setContentsMargins(*[0]*4)
        self._qt_layout.setSpacing(2)
