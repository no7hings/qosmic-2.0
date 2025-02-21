# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

cmd_script = bsc_core.BscFfmpegVideo.generate_video_coding_convert_cmd_script(
    input='Z:/temporaries/camera_mask/maya_avi_1.avi', output='Z:/temporaries/camera_mask/maya_avi_1.mov',
    coding='MPEG4'
)

print(cmd_script)

bsc_core.BscProcess.execute_as_trace(cmd_script)
