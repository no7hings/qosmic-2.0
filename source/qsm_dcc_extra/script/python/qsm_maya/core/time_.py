# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class Frame(object):
    RENDER_ATTR_DICT = {
        'renderer': 'defaultRenderGlobals.currentRenderer',
        'imagePrefix': 'defaultRenderGlobals.imageFilePrefix',
        #
        'start_frame': 'defaultRenderGlobals.startFrame',
        'end_frame': 'defaultRenderGlobals.endFrame',
        #
        'animation': 'defaultRenderGlobals.animation',
        'imageFormat': 'defaultRenderGlobals.imfPluginKey',
        'periodInExt': 'defaultRenderGlobals.periodInExt',
        'putFrameBeforeExt': 'defaultRenderGlobals.putFrameBeforeExt',
        'extensionPadding': 'defaultRenderGlobals.extensionPadding',
        'renderVersion': 'defaultRenderGlobals.renderVersion',
        #
        'width': 'defaultResolution.width',
        'height': 'defaultResolution.height',
        #
        'preMel': 'defaultRenderGlobals.preMel'
    }

    FPS_DICT = {
        '12_fps': '12fps',
        '15_fps': 'game',
        '16_fps': '16fps',
        '24_fps': 'film',
        '25_fps': 'pal',
        '30_fps': 'ntsc',
        '48_fps': 'show',
        '50_fps': 'palf',
        '60_fps': 'ntscf'
    }
    FPS_QUERY_DICT = {v: k for k, v in FPS_DICT.items()}

    @classmethod
    def get_frame_range(cls):
        start_frame = cmds.playbackOptions(query=1, minTime=1)
        end_frame = cmds.playbackOptions(query=1, maxTime=1)
        return int(start_frame), int(end_frame)
    
    @classmethod
    def to_frame_range(cls, frame=None):
        if isinstance(frame, (tuple, list)):
            start_frame, end_frame = frame
        elif isinstance(frame, (int, float)):
            start_frame = end_frame = frame
        else:
            start_frame = end_frame = cls.get_current_frame()
        return int(start_frame), int(end_frame)

    @classmethod
    def auto_range(cls, frame=None):
        if isinstance(frame, (tuple, list)):
            start_frame, end_frame = frame
        elif isinstance(frame, (int, float)):
            start_frame = end_frame = frame
        else:
            start_frame, end_frame = cls.get_frame_range()
        return int(start_frame), int(end_frame)

    @classmethod
    def set_frame_range(cls, start_frame, end_frame):
        cmds.playbackOptions(minTime=start_frame), cmds.playbackOptions(animationStartTime=int(start_frame)-5)
        cmds.playbackOptions(maxTime=end_frame), cmds.playbackOptions(animationEndTime=int(end_frame)+5)
        #
        cls.set_current(start_frame)

    @classmethod
    def set_current(cls, frame):
        cmds.currentTime(frame)

    @classmethod
    def get_current_frame(cls):
        return cmds.currentTime(query=1)

    @classmethod
    def get_fps(cls):
        _ = cmds.currentUnit(query=1, time=1)
        if _ in cls.FPS_QUERY_DICT:
            return cls.FPS_QUERY_DICT[_]

    @classmethod
    def set_fps(cls, fps):
        if fps in cls.FPS_DICT:
            cmds.currentUnit(time=cls.FPS_DICT[fps])

    @classmethod
    def get_render_frame_range(cls):
        start_frame = cmds.getAttr(cls.RENDER_ATTR_DICT['start_frame'])
        end_frame = cmds.getAttr(cls.RENDER_ATTR_DICT['end_frame'])
        return int(start_frame), int(end_frame)
