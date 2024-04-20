# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class Scene(object):
    @classmethod
    def get_frame_range(cls):
        start_frame = int(cmds.playbackOptions(query=1, minTime=1))
        end_frame = int(cmds.playbackOptions(query=1, maxTime=1))
        return start_frame, end_frame
