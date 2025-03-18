# coding:utf-8

import lxbasic.core as bsc_core

from lxgui.qt.core.wrap import *

from .. import base as _base


# connection model
class ConnectionModel(_base._SbjBase):
    ENTITY_TYPE = _base.EntityTypes.Connection

    def __init__(self, gui):
        super(ConnectionModel, self).__init__(gui)

    def get_source(self):
        return self._get_connection_source(self.root_model, self.get_path())

    def get_target(self):
        return self._get_connection_target(self.root_model, self.get_path())

    def do_delete(self):
        self.root_model.remove_connection_path(self.get_path())

    # update
    def update_v(self, *args, **kwargs):
        self._gui._update_v(*args, **kwargs)

    def update_h(self, *args, **kwargs):
        self._gui._update_h(*args, **kwargs)

    def reset_status(self):
        self._gui._set_color(self._gui._default_color)

    def to_correct_status(self):
        self._gui._set_color(QtGui.QColor(0, 255, 0, 255))
