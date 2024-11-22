# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.log as bsc_log

from . import shelf_build as _shelf_build


class MainShelf(object):
    LOG_KEY = 'qosmic shelf'

    MAIN_SHELF_NAME = 'Lazy Tool'
    MAIN_SHELF_KEY = 'Lazy_Tool'

    MAIN_SHELF_NAME_CHS = bsc_core.ensure_unicode('懒人工具')

    OLD_SHELF_NAMES = [
        'QSM',
        MAIN_SHELF_KEY,
        MAIN_SHELF_NAME_CHS
    ]

    def __init__(self):
        pass

    def create(self):
        bsc_log.Log.trace_method_result(
            self.LOG_KEY, 'create'
        )

        _shelf_build.ShelfBuild('maya/lazy-shelf/general').execute()
        # _shelf_build.ShelfBuild('maya/lazy-shelf/animation').execute()
        _shelf_build.ShelfBuild('maya/lazy-shelf/cfx').execute()
