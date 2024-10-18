# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core


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

    # UnitToTimeFactor
    # 2, 3000
    # 3, 2000
    # 4, 1500
    # 5, 1200
    # 12, 500
    # 24, 250
    # 30, 200
    # 60, 100

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
            start_frame = end_frame = cls.get_current_time()
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
        # cls.set_current(start_frame)

    @classmethod
    def update_frame(cls, start_frame, end_frame, frame):
        start_frame_pre, end_frame_pre = cls.get_frame_range()
        if start_frame != start_frame_pre or end_frame != end_frame_pre:
            cls.set_frame_range(start_frame, end_frame)
            cls.set_current(frame)

    @classmethod
    def set_current(cls, frame):
        cmds.currentTime(frame)

    @classmethod
    def get_current_time(cls):
        return cmds.currentTime(query=1)

    @classmethod
    def get_fps_tag(cls):
        _ = cmds.currentUnit(query=1, time=1)
        if _ in cls.FPS_QUERY_DICT:
            return cls.FPS_QUERY_DICT[_]
        else:
            if _.endswith('fps'):
                return _[:-3]+'_fps'

    @classmethod
    def get_fps_value(cls):
        return int(cls.get_fps_tag().split('_')[0])

    @classmethod
    def get_fps_(cls):
        return cmds.currentUnit(query=1, time=1)

    @classmethod
    def set_fps(cls, fps):
        if fps in cls.FPS_DICT:
            cmds.currentUnit(time=cls.FPS_DICT[fps])

    @classmethod
    def get_render_frame_range(cls):
        start_frame = cmds.getAttr(cls.RENDER_ATTR_DICT['start_frame'])
        end_frame = cmds.getAttr(cls.RENDER_ATTR_DICT['end_frame'])
        return int(start_frame), int(end_frame)

    @classmethod
    def get_playback_speed(cls):
        return cmds.playbackOptions(query=1, playbackSpeed=1)

    @classmethod
    def get_playback_info(cls):
        fps = cls.get_fps_tag()
        speed = cls.get_playback_speed()
        if speed == 0:
            return 'Play every frame'
        elif speed > 0:
            return '{} x {}'.format(
                bsc_core.RawTextMtd.to_prettify(fps), speed
            )

    @classmethod
    def set_playback_speed(cls, value):
        cmds.playbackOptions(playbackSpeed=value)
