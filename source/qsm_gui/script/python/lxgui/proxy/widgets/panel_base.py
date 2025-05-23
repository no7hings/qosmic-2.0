# coding:utf-8
from __future__ import print_function

import os

import inspect

import lxbasic.core as bsc_core

import lxbasic.resource as bsc_resource

import lxbasic.content as bsc_content

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

from . import container_for_tab as _container_for_tab


class _ToolBase(object):

    def _init_tool_(self, window):
        self._window = window
        self._configure = self._window._configure
        self._configure_local_flag = False
        self._language = self._window._language

    def _get_subclass_file_path(self):
        frame = inspect.currentframe().f_back
        subclass = frame.f_locals.get('self', None)
        if subclass and isinstance(subclass, self.__class__):
            file_path = inspect.getfile(type(subclass))
            return os.path.abspath(file_path)
        return None

    def generate_local_configure(self):
        self._configure_local_flag = True

        file_path = self._get_subclass_file_path()
        cfg_file_path = '{}.yml'.format(os.path.splitext(file_path)[0].replace('\\', '/'))
        if os.path.isfile(cfg_file_path):
            return bsc_content.Dict(value=cfg_file_path)
        else:
            raise RuntimeError()

    # for language
    def choice_gui_name(self, options):
        return gui_core.GuiUtil.choice_gui_name(
            self._language, options
        )

    def choice_gui_description(self, options):
        return gui_core.GuiUtil.choice_gui_description(
            self._language, options
        )

    def choice_gui_message(self, options):
        return gui_core.GuiUtil.choice_gui_message(
            self._language, options
        )

    def choice_gui_tool_tip(self, options):
        return gui_core.GuiUtil.choice_gui_tool_tip(
            self._language, options
        )


class PrxBasePanel(_window_base.PrxBaseWindow):
    GUI_TYPE = 'window'
    GUI_KEY = 'lazy-tool'

    CONFIGURE_KEY = None

    PAGE_CLASS_DICT = {}
    PAGE_CLASSES = []

    SUBPANEL_CLASS_DICT = {}
    SUBPANEL_CLASSES = []

    def _get_subclass_file_path(self):
        frame = inspect.currentframe().f_back
        subclass = frame.f_locals.get('self', None)
        if subclass and isinstance(subclass, self.__class__):
            file_path = inspect.getfile(type(subclass))
            return os.path.abspath(file_path)
        return None

    def load_local_configure(self):
        file_path = self._get_subclass_file_path()
        cfg_file_path = '{}.yml'.format(os.path.splitext(file_path)[0].replace('\\', '/'))
        if os.path.isfile(cfg_file_path):
            self._configure = bsc_content.Dict(
                value=cfg_file_path
            )
        else:
            raise RuntimeError()

    def __init__(self, window, session, *args, **kwargs):
        super(PrxBasePanel, self).__init__(*args, **kwargs)

        if self.PAGE_CLASS_DICT:
            self._page_class_dict = self.PAGE_CLASS_DICT
        else:
            self._page_class_dict = {}
            if self.PAGE_CLASSES:
                for i_cls in self.PAGE_CLASSES:
                    self._page_class_dict[i_cls.GUI_KEY] = i_cls

        if self.SUBPANEL_CLASS_DICT:
            self._sub_panel_class_dict = self.SUBPANEL_CLASS_DICT
        else:
            self._sub_panel_class_dict = {}
            if self.SUBPANEL_CLASSES:
                for i_cls in self.SUBPANEL_CLASSES:
                    self._sub_panel_class_dict[i_cls.GUI_KEY] = i_cls

        self._gui_path = '/{}'.format(self.GUI_KEY)

        self._init_base_panel_def(window, session, *args, **kwargs)

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
        
        self._tab_widget_dict = {}

    def _gui_main_fnc(self, configure_key):
        if configure_key is None:
            self.load_local_configure()
        else:
            self._configure = bsc_resource.BscConfigure.get_as_content(configure_key)

        self._configure.do_flatten()

        self._option_configure = self._configure.get_as_content('option')
        self._gui_configure = self._configure.get_as_content('option.gui')

        gui_name = gui_core.GuiUtil.choice_gui_name(self._language, self._configure.get('option.gui'))

        python_version = bsc_core.BscSystem.get_python_version()

        core_version = bsc_core.BscEnviron.get_core_version()
        extend_version = bsc_core.BscEnviron.get_extend_version()
        if extend_version:
            window_title = u'{} - ver.{}({}) - python.{}'.format(
                gui_name, core_version, extend_version, python_version
            )
        else:
            window_title = u'{} - ver.{} - python.{}'.format(
                gui_name, core_version, python_version
            )

        self.set_window_title(window_title)
        self.set_window_icon_by_name(
            self._configure.get('option.gui.icon_name')
        )
        self.set_definition_window_size(
            self._configure.get('option.gui.size')
        )

        self.register_window_close_method(self.gui_close_fnc)

        # run delay
        self.start_window_loading(
            self._gui_setup_fnc, post_fnc=self.gui_setup_post_fnc
        )

    def gui_create_tab_tool_box(self):
        prx_tab_tool_box = _container_for_tab.PrxHTabToolBox()
        prx_tab_tool_box.set_history_key(
            [self._window.GUI_KEY, '{}.page'.format(self._gui_path)]
        )

        prx_tab_tool_box.connect_current_changed_to(
            self.do_gui_refresh_all
        )
        return prx_tab_tool_box

    def gui_close_fnc(self):
        pass

    def gui_setup_fnc(self):
        raise NotImplementedError()

    def gui_setup_post_fnc(self):
        pass

    def do_gui_refresh_all(self):
        pass

    def gui_generate_subpanel_for(self, key):
        return self._sub_panel_class_dict[key](self._window, self._session)

    def gui_generate_page_for(self, key):
        return self.gui_instance_page(self._page_class_dict[key])

    def gui_instance_page(self, gui_cls):
        return gui_cls(self._window, self._session)

    def gui_find_page(self, key):
        return self._tab_widget_dict.get(key)

    def show_help_unit(self):
        url_p = self._gui_configure.get('help_url')
        if url_p:
            cfg = bsc_resource.BscConfigure.get_as_content('dokuwiki/main')
            if bsc_core.BscSystem.get_is_dev():
                host = cfg.get('connection_dev.host')
            else:
                host = cfg.get('connection_new.host')

            url = url_p.format(host=host)

            bsc_core.BscSystem.open_url(url)


class PrxBasePage(
    _prx_abstracts.AbsPrxWidget,
    _ToolBase,
):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget

    GUI_TYPE = 'page'
    GUI_KEY = None

    UNIT_CLASS_DICT = {}
    UNIT_CLASSES = []

    def __init__(self, window, session, *args, **kwargs):
        super(PrxBasePage, self).__init__(*args, **kwargs)

        if self.UNIT_CLASS_DICT:
            self._unit_class_dict = self.UNIT_CLASS_DICT
        else:
            self._unit_class_dict = {}
            if self.UNIT_CLASSES:
                for i_cls in self.UNIT_CLASSES:
                    self._unit_class_dict[i_cls.GUI_KEY] = i_cls

        self._init_tool_(window)
        self._session = session

        self._gui_sub_key = self.GUI_KEY
        self._gui_path = '{}/{}'.format(self._window._gui_path, self.GUI_KEY)

        self._tab_widget_dict = {}

        self._qt_layout = _qt_wgt_base.QtVBoxLayout(self._qt_widget)
        self._qt_layout.setContentsMargins(*[0]*4)
        self._qt_layout.setSpacing(2)

    def gui_create_tab_tool_box(self):
        prx_tab_tool_box = _container_for_tab.PrxVTabToolBox()

        prx_tab_tool_box.set_tab_direction(prx_tab_tool_box.TabDirections.RightToLeft)

        prx_tab_tool_box.set_history_key(
            [self._window.GUI_KEY, '{}.page'.format(self._gui_path)]
        )

        prx_tab_tool_box.connect_current_changed_to(
            self.do_gui_refresh_all
        )
        return prx_tab_tool_box

    def gui_setup_units_for(self, prx_tab_tool_box, keys):
        self._tab_widget_dict = {}

        for i_cls in self.UNIT_CLASSES:
            i_key = i_cls.GUI_KEY
            if i_cls.GUI_KEY in keys:
                i_gui = i_cls(self._window, self, self._session)

                prx_tab_tool_box.add_widget(
                    i_gui,
                    key=i_key,
                    name=gui_core.GuiUtil.choice_gui_name(
                        self._window._language, self._window._configure.get(
                            'build.{}.{}'.format(self._gui_sub_key, i_gui.GUI_KEY)
                        )
                    ),
                    icon_name_text=i_key,
                    tool_tip=gui_core.GuiUtil.choice_gui_tool_tip(
                        self._window._language, self._window._configure.get(
                            'build.{}.{}'.format(self._gui_sub_key, i_gui.GUI_KEY)
                        )
                    )
                )

                self._tab_widget_dict[i_key] = i_gui

        prx_tab_tool_box.load_history()

    def do_gui_refresh_unit_auto(self, prx_tab_tool_box):
        key = prx_tab_tool_box.get_current_key()
        gui = self._tab_widget_dict.get(key)
        if gui:
            gui.do_gui_refresh_all()

    def gui_page_setup_fnc(self):
        """
        main setup function put here
        """

    def gui_setup_post_fnc(self):
        """
        fix some size bug for size setup delay
        """

    def gui_generate_unit_for(self, key):
        return self.gui_instance_unit(self._unit_class_dict[key])

    def gui_instance_unit(self, gui_cls):
        return gui_cls(self._window, self, self._session)

    def _to_unit_instance(self, cls):
        return cls(self._window, self, self._session)

    def do_gui_refresh_all(self):
        pass

    def get_gui_name(self):
        if self._configure_local_flag is True:
            # use for local
            return self.choice_gui_name(
                self._configure.get('build')
            )
        return self.choice_gui_name(
            self._configure.get('build.{}'.format(self.GUI_KEY))
        )

    def get_gui_tool_tip(self):
        if self._configure_local_flag is True:
            # use for local
            return self.choice_gui_tool_tip(
                self._configure.get('build')
            )
        return self.choice_gui_tool_tip(
            self._configure.get('build.{}'.format(self.GUI_KEY))
        )


class PrxBaseUnit(
    _prx_abstracts.AbsPrxWidget,
    _ToolBase,
):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget

    GUI_KEY = None

    TOOLSET_CLASS_DICT = {}
    TOOLSET_CLASSES = []

    def __init__(self, window, page, session, *args, **kwargs):
        super(PrxBaseUnit, self).__init__(*args, **kwargs)

        if self.TOOLSET_CLASS_DICT:
            self._toolset_class_dict = self.TOOLSET_CLASS_DICT
        else:
            self._toolset_class_dict = {}
            if self.TOOLSET_CLASSES:
                for i_cls in self.TOOLSET_CLASSES:
                    self._toolset_class_dict[i_cls.GUI_KEY] = i_cls

        self._init_tool_(window)
        self._page = page
        self._session = session

        self._tab_widget_dict = {}

        self._gui_sub_key = '{}.{}'.format(
            self._page.GUI_KEY, self.GUI_KEY
        )
        self._gui_path = '{}/{}'.format(self._page._gui_path, self.GUI_KEY)

        self._qt_layout = _qt_wgt_base.QtVBoxLayout(self._qt_widget)
        self._qt_layout.setContentsMargins(*[0]*4)
        self._qt_layout.setSpacing(2)

        self._window.register_window_close_method(self.gui_close_fnc)

    def gui_create_tab_tool_box(self):
        prx_tab_tool_box = _container_for_tab.PrxVTabToolBox()

        prx_tab_tool_box.set_tab_direction(prx_tab_tool_box.TabDirections.RightToLeft)

        prx_tab_tool_box.set_history_key(
            [self._window.GUI_KEY, '{}.page'.format(self._gui_path)]
        )

        prx_tab_tool_box.connect_current_changed_to(
            self.do_gui_refresh_all
        )
        return prx_tab_tool_box

    def gui_find_page(self, key):
        return self._tab_widget_dict.get(key)

    def gui_unit_setup_fnc(self):
        pass

    def gui_setup_post_fnc(self):
        pass

    def do_gui_refresh_all(self):
        pass

    def do_gui_refresh_toolsets(self):
        pass

    def gui_close_fnc(self):
        pass


class PrxVirtualBaseUnit(_ToolBase):
    GUI_KEY = None

    def __init__(self, window, page, session):
        self._init_tool_(window)
        self._page = page
        self._session = session

        self._gui_sub_key = '{}.{}'.format(
            self._page.GUI_KEY, self.GUI_KEY
        )
        self._gui_path = '{}/{}'.format(
            self._page._gui_path, self.GUI_KEY
        )

    def do_gui_refresh_all(self):
        pass


class PrxVirtualBaseSubunit(_ToolBase):
    GUI_KEY = None

    def __init__(self, window, page, unit, session):
        self._init_tool_(window)
        self._page = page
        self._unit = unit
        self._session = session

        self._gui_sub_key = '{}.{}.{}'.format(
            self._page.GUI_KEY, self._unit.GUI_KEY, self.GUI_KEY
        )
        self._gui_path = '{}/{}'.format(
            self._unit._gui_path, self.GUI_KEY
        )

    def do_gui_refresh_all(self):
        pass


class PrxBaseSubpanel(_window_base.PrxBaseWindow):
    CONFIGURE_KEY = None

    GUI_KEY = None

    SUB_PAGE_CLASS_DICT = {}
    SUBPAGE_CLASSES = []

    SUB_PAGE_KEYS = []

    def _get_subclass_file_path(self):
        frame = inspect.currentframe().f_back
        subclass = frame.f_locals.get('self', None)
        if subclass and isinstance(subclass, self.__class__):
            file_path = inspect.getfile(type(subclass))
            return os.path.abspath(file_path)
        return None

    def load_local_configure(self):
        file_path = self._get_subclass_file_path()
        cfg_file_path = '{}.yml'.format(os.path.splitext(file_path)[0].replace('\\', '/'))
        if os.path.isfile(cfg_file_path):
            self._configure = bsc_content.Dict(
                value=cfg_file_path
            )
        else:
            raise RuntimeError()

    def __init__(self, window, session, *args, **kwargs):
        super(PrxBaseSubpanel, self).__init__(*args, **kwargs)

        if self.SUB_PAGE_CLASS_DICT:
            self._subpage_class_dict = self.SUB_PAGE_CLASS_DICT
        else:
            self._subpage_class_dict = {}
            if self.SUBPAGE_CLASSES:
                for i_cls in self.SUBPAGE_CLASSES:
                    self._subpage_class_dict[i_cls.GUI_KEY] = i_cls

        self._tab_widget_dict = {}

        self._init_base_panel_def(window, session, *args, **kwargs)

    def _gui_setup_fnc(self):
        self.gui_setup_fnc()

    def _init_base_panel_def(self, window, session, *args, **kwargs):
        self._window = window

        if self._window is not None:
            self._qt_widget.setParent(window._qt_widget, gui_qt_core.QtCore.Qt.Tool)
            self._qt_widget.setWindowFlags(gui_qt_core.QtCore.Qt.Tool)
            self._gui_path = '{}/{}'.format(self._window._gui_path, self.GUI_KEY)
        else:
            self._gui_path = '/{}'.format(self.GUI_KEY)

        self._session = session

        self._subwindow = self

        self._language = gui_core.GuiUtil.get_language()

        self._gui_debug_run(
            self._gui_main_fnc, self.CONFIGURE_KEY
        )

    def _gui_main_fnc(self, configure_key):
        if configure_key is None:
            self.load_local_configure()
        else:
            self._configure = bsc_resource.BscConfigure.get_as_content(configure_key)

        self._option_configure = self._configure.get_as_content('option')
        self._gui_configure = self._configure.get_as_content('option.gui')

        self.set_window_title(
            gui_core.GuiUtil.choice_gui_name(self._language, self._configure.get('option.gui'))
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

    def gui_generate_subpage_for(self, key):
        return self.gui_instance_subpage(self._subpage_class_dict[key])

    def gui_instance_subpage(self, gui_cls):
        return gui_cls(self._window, self._session, self)

    def gui_find_page(self, key):
        return self._tab_widget_dict.get(key)

    def do_gui_refresh_all(self):
        pass


class PrxBaseSubpage(
    _prx_abstracts.AbsPrxWidget,
    _ToolBase,
):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget

    GUI_KEY = None

    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(PrxBaseSubpage, self).__init__(*args, **kwargs)

        self._init_tool_(window)

        self._session = session
        self._subwindow = subwindow

        self._gui_path = '{}/{}'.format(self._subwindow._gui_path, self.GUI_KEY)

        self._qt_layout = _qt_wgt_base.QtVBoxLayout(self._qt_widget)
        self._qt_layout.setContentsMargins(*[0]*4)
        self._qt_layout.setSpacing(2)

    def gui_page_setup_fnc(self):
        """
        main setup function put here
        """

    def do_gui_refresh_all(self):
        pass

    def get_gui_name(self):
        if self._configure_local_flag is True:
            # use for local
            return self.choice_gui_name(
                self._configure.get('build')
            )
        return self.choice_gui_name(
            self._configure.get('build.{}'.format(self.GUI_KEY))
        )

    def get_gui_tool_tip(self):
        if self._configure_local_flag is True:
            # use for local
            return self.choice_gui_tool_tip(
                self._configure.get('build')
            )
        return self.choice_gui_tool_tip(
            self._configure.get('build.{}'.format(self.GUI_KEY))
        )
