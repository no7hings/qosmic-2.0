# coding:utf-8
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import lxbasic.core as bsc_core

import qsm_maya.core as qsm_mya_core


class HUD(object):
    timeConfig = dict(
        game='15 FPS',
        film='24 FPS',
        pal='25 FPS',
        ntsc='30 FPS',
        sho='48 FPS',
        palf='50 FPS',
        ntscf='60 FPS'
    )

    @classmethod
    def get_camera(cls, camera_path=None):
        if qsm_mya_core.Scene.get_is_ui_mode():
            return qsm_mya_core.DagNode.to_name(
                qsm_mya_core.Camera.get_active()
            )
        return qsm_mya_core.DagNode.to_name(camera_path)

    @classmethod
    def get_fps_tag(cls):
        time_unit = qsm_mya_core.Frame.get_time_unit()
        return cls.timeConfig[time_unit]

    @classmethod
    def get_user(cls):
        return bsc_core.BscSystem.get_user_name()

    @classmethod
    def get_frame(cls):
        start_frame = int(cmds.playbackOptions(query=1, min=1))
        end_frame = int(cmds.playbackOptions(query=1, max=1))
        current_frame = int(cmds.currentTime(query=1))
        c = len(str(end_frame))
        index = current_frame-start_frame+1
        index_max = end_frame-start_frame+1
        return '{current_frame} / ({start_frame}-{end_frame}) | {index} / {index_max}'.format(
            index=str(index).zfill(c), index_max=str(index_max).zfill(c), current_frame=str(current_frame).zfill(c),
            start_frame=start_frame, end_frame=end_frame
        )

    @classmethod
    def get_time(cls):

        time_unit = qsm_mya_core.Frame.get_time_unit()
        #
        start_frame = cmds.playbackOptions(query=1, min=1)
        end_frame = cmds.playbackOptions(query=1, max=1)
        current_frame = cmds.currentTime(query=1)
        time_range = '%.2f' % ((end_frame-start_frame)/int(cls.timeConfig[time_unit][:2]))
        frame = current_frame-start_frame
        time_max = '%.2f' % (frame/int(cls.timeConfig[time_unit][:2]))
        c = len(str(time_range))
        return '%s / %s' % (str(time_max).zfill(c), str(time_range).zfill(c))

    @classmethod
    def get_resolution(cls):
        return '{} x {}'.format(*qsm_mya_core.RenderSettings.get_resolution())

    @classmethod
    def generate_configure(cls, camera_path=None):
        return {
            'fps': dict(
                section=0,
                block=0,
                blockAlignment='center',
                labelFontSize='small',
                dataFontSize='small',
                blockSize='medium',
                label='FPS: ',
                labelWidth=64,
                command=lambda: cls.get_fps_tag(),
                attachToRefresh=1
            ),
            'resolution': dict(
                section=2,
                block=0,
                blockAlignment='center',
                labelFontSize='small',
                dataFontSize='small',
                blockSize='medium',
                label='resolution: ',
                labelWidth=64,
                # dataAlignment='left',
                # dataWidth=96,
                command=lambda: cls.get_resolution(),
                attachToRefresh=1
            ),
            'frame': dict(
                section=4,
                block=0,
                blockAlignment='center',
                labelFontSize='small',
                dataFontSize='small',
                blockSize='medium',
                label='frame: ',
                labelWidth=64,
                command=lambda: cls.get_frame(),
                attachToRefresh=1
            ),
            'user': dict(
                section=5,
                block=0,
                blockAlignment='center',
                labelFontSize='small',
                dataFontSize='small',
                blockSize='small',
                label='user: ',
                labelWidth=64,
                command=lambda: cls.get_user(),
                attachToRefresh=1
            ),
            'camera': dict(
                section=7,
                block=0,
                blockAlignment='center',
                labelFontSize='small',
                dataFontSize='small',
                blockSize='small',
                label='camera: ',
                labelWidth=64,
                command=lambda: cls.get_camera(camera_path),
                attachToRefresh=1
            ),
            'date': dict(
                section=9,
                block=0,
                blockAlignment='center',
                labelFontSize='small',
                dataFontSize='small',
                blockSize='small',
                label='date: ',
                labelWidth=64,
                command=lambda: bsc_core.BscSystem.get_time(),
                attachToRefresh=1
            )
        }

    @classmethod
    def set_color(cls, key_color=19, value_color=16):
        if cmds.displayColor("headsUpDisplayLabels", q=1, dormant=1):
            # noinspection PyBroadException
            try:
                cmds.displayColor('headsUpDisplayLabels', key_color, dormant=1)
            except Exception:
                pass

        if cmds.displayColor('headsUpDisplayValues', q=1, dormant=1):
            # noinspection PyBroadException
            try:
                cmds.displayColor('headsUpDisplayValues', value_color, dormant=1)
            except Exception:
                pass

    @classmethod
    def create(cls, camera_path=None):
        config = cls.generate_configure(camera_path)
        for k, v in config.items():
            cmds.headsUpDisplay(
                k, **v
            )
        #
        cls.set_color()

    @classmethod
    def restore(cls):
        config = cls.generate_configure()
        for k, v in config.items():
            if cmds.headsUpDisplay(k, query=1, exists=1):
                cmds.headsUpDisplay(k, remove=1)
