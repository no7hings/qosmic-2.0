# coding:utf-8
import sys

import six

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage
# gui
from ... import core as gui_core
# qt
from .wrap import *

from . import base as _base


class AbsGuiDcc(object):
    @classmethod
    def get_is_maya(cls):
        return gui_core.GuiUtil.get_is_maya()

    @classmethod
    def get_is_houdini(cls):
        return gui_core.GuiUtil.get_is_houdini()

    @classmethod
    def get_is_katana(cls):
        return gui_core.GuiUtil.get_is_katana()

    @classmethod
    def get_is_clarisse(cls):
        return gui_core.GuiUtil.get_is_clarisse()


class QtMaya(object):
    @classmethod
    def to_qt_object(cls, ptr, base=QtWidgets.QWidget):
        # noinspection PyUnresolvedReferences
        from shiboken2 import wrapInstance
        if six.PY2:
            # noinspection PyCompatibility
            return wrapInstance(long(ptr), base)
        return wrapInstance(int(ptr), base)

    @classmethod
    def get_qt_menu_bar(cls):
        qt_main_window = cls.get_qt_main_window()
        if qt_main_window:
            children = qt_main_window.children()
            for i_child in children:
                if i_child:
                    if isinstance(i_child, QtWidgets.QMenuBar):
                        return i_child

    @classmethod
    def get_qt_menu(cls, text):
        qt_menu_bar = cls.get_qt_menu_bar()
        if qt_menu_bar:
            children = qt_menu_bar.children()
            for i_child in children:
                if isinstance(i_child, QtWidgets.QMenu):
                    i_name = i_child.title()
                    if i_name == text:
                        return i_child

    @classmethod
    def get_qt_main_window(cls):
        # noinspection PyUnresolvedReferences
        from maya import OpenMayaUI

        #
        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window:
            return cls.to_qt_object(
                main_window,
                QtWidgets.QMainWindow
            )

    @classmethod
    def generate_qt_icon_by_name(cls, icon_name):
        # noinspection PyUnresolvedReferences
        from maya import OpenMayaUI

        ptr = OpenMayaUI.MQtUtil.createIcon(icon_name)
        if ptr is None:
            ptr = OpenMayaUI.MQtUtil.createIcon('default')
        return cls.to_qt_object(ptr, QtGui.QIcon)

    @classmethod
    def find_all_qt_widgets_by_class(cls, *args, **kwargs):
        return _base.QtUtil.find_all_qt_widgets_by_class(*args, **kwargs)

    @classmethod
    def make_snapshot(cls, file_path):
        bsc_storage.StgFileOpt(file_path).create_directory()

        main_window = cls.get_qt_main_window()
        # s = QtGui.QPixmap.grabWindow(
        #     long(main_window.winId())
        # )
        rect = main_window.rect()

        app_ = QtWidgets.QApplication
        # noinspection PyArgumentList
        image = QtGui.QPixmap.grabWindow(
            app_.desktop().winId()
        ).copy(rect).toImage()

        # _base.QtUtil.save_qt_image(image, file_path)
        image.save(file_path)

    @classmethod
    def create_window_shortcut_action(cls, fnc, shortcut):
        main_window = cls.get_qt_main_window()
        act = QtWidgets.QAction(main_window)
        # noinspection PyUnresolvedReferences
        act.triggered.connect(fnc)
        act.setShortcut(QtGui.QKeySequence(shortcut))
        act.setShortcutContext(QtCore.Qt.WindowShortcut)
        main_window.addAction(act)


class QtHoudini(object):
    @classmethod
    def get_qt_main_window(cls):
        # noinspection PyUnresolvedReferences
        import hou

        return hou.qt.mainWindow()

    @classmethod
    def generate_qt_icon_by_name(cls, icon_name):
        # noinspection PyUnresolvedReferences
        import hou

        if icon_name is not None:
            return hou.qt.Icon(icon_name)
        return hou.qt.Icon('MISC_python')

    @classmethod
    def make_snapshot(cls, file_path):
        bsc_storage.StgFileOpt(file_path).create_directory()

        main_window = cls.get_qt_main_window()
        rect = main_window.rect()

        app_ = QtWidgets.QApplication
        # noinspection PyArgumentList
        image = QtGui.QPixmap.grabWindow(
            app_.desktop().winId()
        ).copy(rect).toImage()

        # _base.QtUtil.save_qt_image(image, file_path)
        image.save(file_path)


class QtKatana(object):
    @classmethod
    def get_qt_main_window(cls):
        # noinspection PyUnresolvedReferences
        import UI4

        return UI4.App.MainWindow.GetMainWindow()

    @classmethod
    def generate_qt_icon_by_name(cls, icon_name):
        # noinspection PyUnresolvedReferences
        import UI4

        return UI4.Util.ScenegraphIconManager.GetIcon(icon_name, 32)

    @classmethod
    def get_menu_bar(cls):
        main_window = cls.get_qt_main_window()
        if main_window is None:
            bsc_log.Log.trace_method_warning(
                'qt-katana',
                'main-window is non-exists'
            )
            return
        #
        return main_window.getMenuBar()

    @classmethod
    def get_menu(cls, name):
        menu_bar = cls.get_menu_bar()
        if menu_bar is None:
            bsc_log.Log.trace_method_warning(
                'qt-katana',
                'menu-bar is non-exists'
            )
            return
        #
        for i_child in menu_bar.children():
            if isinstance(i_child, QtWidgets.QMenu):
                i_name = i_child.title()
                if i_name == name:
                    return i_child

    @classmethod
    def make_snapshot(cls, file_path):
        bsc_storage.StgFileOpt(file_path).create_directory()
        main_window = cls.get_qt_main_window()
        rect = main_window.rect()

        app_ = QtWidgets.QApplication
        # noinspection PyArgumentList
        screen = app_.primaryScreen()

        pixmap = screen.grabWindow(main_window.winId())
        image = pixmap.copy(rect).toImage()

        image.save(file_path)
        # _base.QtUtil.save_qt_image(image, file_path)


class GuiQtClarisse(object):
    QT_MAIN_WINDOW = None

    @classmethod
    def get_qt_main_window(cls):
        return None

    @classmethod
    def get_qt_main_window_geometry_args(cls):
        # noinspection PyUnresolvedReferences
        import ix

        x, y = ix.application.get_event_window().get_position()
        w, h = ix.application.get_event_window().get_size()
        return x, y, w, h


class GuiQtDcc(AbsGuiDcc):
    QT_MAIN_WINDOW = None
    QT_PALETTE_CACHE = None

    @classmethod
    def get_qt_main_window(cls):
        if cls.get_is_maya():
            return QtMaya.get_qt_main_window()
        elif cls.get_is_houdini():
            return QtHoudini.get_qt_main_window()
        elif cls.get_is_katana():
            return QtKatana.get_qt_main_window()
        elif cls.get_is_clarisse():
            return GuiQtClarisse.get_qt_main_window()
        #
        if cls.QT_MAIN_WINDOW is not None:
            return cls.QT_MAIN_WINDOW
        #
        # noinspection PyArgumentList
        _ = QtWidgets.QApplication.topLevelWidgets()
        if _:
            cls.QT_MAIN_WINDOW = _[0]
        return _base.QtUtil.get_qt_active_window()

    @classmethod
    def get_qt_active_window(cls):
        return _base.QtUtil.get_qt_active_window()

    @classmethod
    def generate_qt_icon_by_name(cls, icon_name):
        if cls.get_is_maya():
            return QtMaya.generate_qt_icon_by_name(icon_name)
        elif cls.get_is_houdini():
            return QtHoudini.generate_qt_icon_by_name(icon_name)
        return _base.QtIcon.generate_by_name(icon_name)

    @classmethod
    def generate_qt_directory_icon(cls, use_system=False):
        f_i_p = QtWidgets.QFileIconProvider()
        if use_system is True:
            return f_i_p.icon(f_i_p.Folder)
        return _base.QtIcon.generate_by_icon_name('file/folder')

    @classmethod
    def generate_qt_file_icon(cls, file_path):
        f_i_p = QtWidgets.QFileIconProvider()
        if bsc_storage.StgPath.get_is_file(file_path) is True:
            info = QtCore.QFileInfo(file_path)
            return f_i_p.icon(info)
        return f_i_p.icon(f_i_p.File)

    @classmethod
    def generate_qt_palette(cls):
        def fnc_():
            if cls.get_is_maya():
                return _base.QtUtil.generate_qt_palette()
            elif cls.get_is_houdini():
                return _base.QtUtil.generate_qt_palette()
            elif cls.get_is_katana():
                return _base.QtUtil.generate_qt_palette()
            elif cls.get_is_clarisse():
                return _base.QtUtil.generate_qt_palette(tool_tip=True)
            return _base.QtUtil.generate_qt_palette(tool_tip=True)

        if cls.QT_PALETTE_CACHE is not None:
            return cls.QT_PALETTE_CACHE

        cls.QT_PALETTE_CACHE = fnc_()
        return cls.QT_PALETTE_CACHE

    @classmethod
    def exit_app(cls, app):
        if cls.get_is_clarisse():
            # noinspection PyUnresolvedReferences
            import pyqt_clarisse

            pyqt_clarisse.exec_(app)
        else:
            sys.exit(app.exec_())

    @classmethod
    def get_qt_main_window_geometry_args(cls):
        if cls.get_is_clarisse():
            return GuiQtClarisse.get_qt_main_window_geometry_args()
