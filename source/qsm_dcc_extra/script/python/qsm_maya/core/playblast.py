# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.storage as bsc_storage


class Playblast(object):
    @classmethod
    def make_snapshot(cls, file_path, frame, size):
        file_opt = bsc_storage.StgFileOpt(file_path)
        if file_opt.get_is_exists() is True:
            file_opt.do_delete()
        result = cmds.playblast(
            startTime=frame,
            endTime=frame,
            format='image',
            filename=file_opt.get_path_base(),
            sequenceTime=0,
            clearCache=1,
            viewer=0,
            showOrnaments=1,
            offScreen=0,
            framePadding=4,
            percent=100,
            compression=file_opt.get_format(),
            quality=100,
            widthHeight=size,
        )
        results = bsc_storage.StgFileTiles.get_tiles(result)
        if results:
            bsc_storage.StgFileOpt(results[0]).repath_to(file_path)
