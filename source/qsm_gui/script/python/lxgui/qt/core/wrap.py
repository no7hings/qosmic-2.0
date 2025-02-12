# coding:utf-8
import sys as _sys

import cgitb as _cgitb

import pkgutil as _pkgutil

import importlib as _importlib

import lxbasic.log as _log_core

QT_LOAD_INDEX = None
QT_LOAD_FLAG = None
QtSide = None

__pyqt5 = _pkgutil.find_loader('PyQt5')
if __pyqt5 is not None:
    QT_LOAD_INDEX = 0
    QT_LOAD_FLAG = 'pyqt'
    # noinspection PyUnresolvedReferences
    from PyQt5 import QtGui, QtCore, QtWidgets, QtSvg, QtWebSockets
    # noinspection PyUnresolvedReferences
    from PyQt5 import QtMultimedia

    _sys.modules['QtSide'] = _sys.modules['PyQt5']
    _log_core.Log.trace_method_result(
        'qt wrap', 'load form "PyQt5"'
    )
else:
    __pyside2 = _pkgutil.find_loader('PySide2')
    if __pyside2 is not None:
        QT_LOAD_INDEX = 1
        QT_LOAD_FLAG = 'pyside'
        # noinspection PyUnresolvedReferences
        from PySide2 import QtGui, QtCore, QtWidgets, QtSvg, QtWebSockets
        # noinspection PyUnresolvedReferences
        from PySide2 import QtMultimedia

        _sys.modules['QtSide'] = _sys.modules['PySide2']
        _log_core.Log.trace_method_result(
            'qt wrap', 'load form "PySide2"'
        )


if QT_LOAD_INDEX is None:
    raise ImportError(
        _log_core.Log.trace_error(
            'neither "PyQt5" or "PySide2" is found'
        )
    )


_log_directory_path = _log_core.LogBase.get_user_debug_directory(
    tag='qt', create=True
)

_cgitb.enable(
    logdir=_log_directory_path,
    format='text'
)

_log_core.Log.trace_method_result(
    'qt wrap', 'register log at: {}'.format(_log_directory_path)
)

load_dic = {
    'qt_property': [
        ("PyQt5.QtCore", "pyqtProperty"),
        ("PySide2.QtCore", "Property"),
        ("PySide2.QtCore", "Property")
    ],
    'qt_signal': [
        ("PyQt5.QtCore", "pyqtSignal"),
        ("PySide2.QtCore", "Signal"),
        ("PySide2.QtCore", "Signal")
    ],
    'qt_wrapinstance': [
        ("sip", "wrapinstance"),
        ("shiboken2", "wrapInstance"),
        ("PySide2.shiboken2", "wrapInstance")
    ],
    'qt_is_deleted': [
        ("sip", "isdeleted"),
        ("shiboken2", "isValid"),
        ("PySide2.shiboken2", "isValid")
    ],
    'qt_slot': [
        ("PyQt5.QtCore", "pyqtSlot"),
        ("PySide2.QtCore", "Slot"),
        ("PySide2.QtCore", "Slot")
    ]
}

misplaced_dic = {
    "QtCore.pyqtProperty": "QtCore.Property",
    "QtCore.pyqtSignal": "QtCore.Signal",
    "QtCore.pyqtSlot": "QtCore.Slot",
    "QtCore.QAbstractProxyModel": "QtCore.QAbstractProxyModel",
    "QtCore.QSortFilterProxyModel": "QtCore.QSortFilterProxyModel",
    "QtCore.QStringListModel": "QtCore.QStringListModel",
    "QtCore.QItemSelection": "QtCore.QItemSelection",
    "QtCore.QItemSelectionModel": "QtCore.QItemSelectionModel",
    "QtCore.QItemSelectionRange": "QtCore.QItemSelectionRange",
    "uic.loadUi": "QtCompat.loadUi",
    "sip.wrapinstance": "QtCompat.wrapInstance",
    "sip.unwrapinstance": "QtCompat.getCppPointer",
    "sip.isdeleted": "QtCompat.isValid",
    "QtWidgets.qApp": "QtWidgets.QApplication.instance()",
    "QtCore.QCoreApplication.translate": "QtCompat.translate",
    "QtWidgets.QApplication.translate": "QtCompat.translate",
    "QtCore.qInstallMessageHandler": "QtCompat.qInstallMessageHandler",
    "QtWidgets.QStyleOptionViewItem": "QtCompat.QStyleOptionViewItemV4",
}


class __Loader(object):
    def __init__(self, module_name):
        self.__module = _importlib.import_module(module_name)

    def get_method(self, key):
        return self.__module.__dict__[key]


def qt_signal(*args):
    # noinspection PyUnresolvedReferences
    module_name, method_name = load_dic[_sys._getframe().f_code.co_name][QT_LOAD_INDEX]
    return __Loader(module_name).get_method(method_name)(*args)


def qt_slot(*args):
    # noinspection PyUnresolvedReferences
    module_name, method_name = load_dic[_sys._getframe().f_code.co_name][QT_LOAD_INDEX]
    return __Loader(module_name).get_method(method_name)(*args)


def qt_wrapinstance(*args):
    # noinspection PyUnresolvedReferences
    module_name, method_name = load_dic[_sys._getframe().f_code.co_name][QT_LOAD_INDEX]
    return __Loader(module_name).get_method(method_name)(*args)


def qt_is_deleted(*args):
    # noinspection PyUnresolvedReferences
    module_name, method_name = load_dic[_sys._getframe().f_code.co_name][QT_LOAD_INDEX]
    return __Loader(module_name).get_method(method_name)(*args)


def qt_rect(*args):
    class _QRect(QtCore.QRect):
        def __init__(self, *_args):
            super(_QRect, self).__init__(*_args)

        def setRect(self, *_args):
            return super(_QRect, self).setRect(
                *map(int, _args)
            )
    if args:
        if len(args) == 4:
            # convert to int
            x, y, w, h = args
            return _QRect(int(x), int(y), int(w), int(h))
        return _QRect(*args)
    return _QRect()
