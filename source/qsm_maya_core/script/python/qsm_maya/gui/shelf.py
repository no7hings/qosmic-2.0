# coding:utf-8
import lxbasic.log as bsc_log

from . import shelf_build as _shelf_build


class MayaShelf(object):
    LOG_KEY = 'qosmic shelf'

    def __init__(self):
        pass

    def create(self):
        bsc_log.Log.trace_method_result(
            self.LOG_KEY, 'create'
        )

        _shelf_build.ShelfBuild('maya/shelves/general').execute()
        _shelf_build.ShelfBuild('maya/shelves/animation').execute()
        _shelf_build.ShelfBuild('maya/shelves/cfx').execute()
