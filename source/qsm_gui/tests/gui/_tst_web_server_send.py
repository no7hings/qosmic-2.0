# coding:utf-8
import lxgui.qt.core as gui_qt_core

if gui_qt_core.WebSocketConnection.check_is_exists() is True:
    for i in range(2):
        # gui_qt_core.WebSocketConnection().send(
        #     'python("print \\\"{}\\\"")'.format(i)
        # )
        gui_qt_core.WebSocketConnection().send(
            '拍屏结束了，是否播放文件: {}'.format(i)
        )
