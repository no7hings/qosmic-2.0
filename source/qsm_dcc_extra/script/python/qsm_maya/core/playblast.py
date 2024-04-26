# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class Playblast(object):
    @classmethod
    def save_snapshot(cls, file_path, size):
        cmds.playblast(
            startTime=1,
            endTime=1,
            format='image',
            filename='Z:/projects/QSM_TST/workarea/dev.developing/resource_manager/.snapshot/test',
            sequenceTime=0,
            clearCache=1,
            viewer=0,
            showOrnaments=1,
            offScreen=0,
            framePadding=4,
            percent=100,
            compression='jpg',
            quality=100,
            widthHeight=(480, 320),
        )
