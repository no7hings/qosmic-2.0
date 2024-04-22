# coding:utf-8
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds


class Time(object):
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
    def set_frame_range(cls, star_frame, end_frame):
        cmds.playbackOptions(minTime=star_frame), cmds.playbackOptions(animationStartTime=int(star_frame)-5)
        cmds.playbackOptions(maxTime=end_frame), cmds.playbackOptions(animationEndTime=int(end_frame)+5)
        #
        cls.set_current_frame(star_frame)

    @classmethod
    def set_current_frame(cls, frame):
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


class File(object):
    FILE_TYPE_ASCII = 'mayaAscii'
    FILE_TYPE_BINARY = 'mayaBinary'
    FILE_TYPE_ALEMBIC = 'Alembic'

    FILE_TYPE_DICT = {
        '.ma': FILE_TYPE_ASCII,
        '.mb': FILE_TYPE_BINARY,
        '.abc': FILE_TYPE_ALEMBIC
    }

    @classmethod
    def _get_file_type_name_(cls, file_path):
        ext = os.path.splitext(file_path)[-1]
        return cls.FILE_TYPE_DICT.get(ext, cls.FILE_TYPE_ASCII)

    @classmethod
    def reference_file(cls, file_path, namespace=':'):
        if os.path.isfile(file_path) is True:
            return cmds.file(
                file_path,
                ignoreVersion=1,
                reference=1,
                mergeNamespacesOnClash=0,
                namespace=namespace,
                options='v=0;',
                type=cls._get_file_type_name_(file_path)
            )

    @classmethod
    def import_file(cls, file_path, namespace=':'):
        if os.path.isfile(file_path) is True:
            return cmds.file(
                file_path,
                i=True,
                options='v=0;',
                type=cls._get_file_type_name_(file_path),
                ra=True,
                mergeNamespacesOnClash=True,
                namespace=namespace,
            )


class Scene(
    Time,
    File
):
    @classmethod
    def show_message(cls, message, keyword, position='topCenter', fade=1, drag_kill=0, alpha=.5):
        # topLeft topCenter topRight
        # midLeft midCenter midCenterTop midCenterBot midRight
        # botLeft botCenter botRight
        cmds.inViewMessage(
            assistMessage='%s <hl>%s</hl>'%(message, keyword),
            fontSize=12,
            position=position,
            fade=fade,
            dragKill=drag_kill,
            alpha=alpha
        )
