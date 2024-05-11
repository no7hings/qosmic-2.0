# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class RenderSettings(object):
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

    @classmethod
    def set_frame_range(cls, start_frame=None, end_frame=None):
        if not start_frame:
            start_frame = int(cmds.playbackOptions(query=1, minTime=1))
        if not end_frame:
            end_frame = int(cmds.playbackOptions(query=1, maxTime=1))
        #
        cmds.setAttr(cls.RENDER_ATTR_DICT['start_frame'], start_frame)
        cmds.setAttr(cls.RENDER_ATTR_DICT['end_frame'], end_frame)

    @classmethod
    def get_frame_range(cls):
        start_frame = cmds.getAttr(cls.RENDER_ATTR_DICT['start_frame'])
        end_frame = cmds.getAttr(cls.RENDER_ATTR_DICT['end_frame'])
        return int(start_frame), int(end_frame)

    @classmethod
    def set_resolution(cls, width, height):
        cmds.setAttr(cls.RENDER_ATTR_DICT['width'], width)
        cmds.setAttr(cls.RENDER_ATTR_DICT['height'], height)
        if width == height:
            cmds.setAttr('defaultResolution.deviceAspectRatio', 1)
        cmds.setAttr('defaultResolution.pixelAspect', 1)

    @classmethod
    def get_resolution(cls):
        width = cmds.getAttr(cls.RENDER_ATTR_DICT['width'])
        height = cmds.getAttr(cls.RENDER_ATTR_DICT['height'])
        return int(width), int(height)


class HardwareRenderSettings(object):
    @classmethod
    def open_gpu_instancing(cls):
        cmds.setAttr(
            'hardwareRenderingGlobals.hwInstancing', 1
        )
