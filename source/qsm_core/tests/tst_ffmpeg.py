# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

# print bsc_storage.StgFileOpt(
#     'F:/video/film/Batman.v.Superman.Dawn.of.Justice[蝙蝠侠大战超人：正义黎明][加长版]/[47BT]蝙蝠侠大战超人.正义黎明.Batman.v.Superman.Dawn.of.Justice.BluRay.2160p.10Bit.HDR.HEVC.DDP5.1.2Audio.mkv'
# ).get_size_as_gb()


# print bsc_core.BscFfmpeg.get_frame_args(
#     'Z:/temeporaries/dongchangbao/snapshot/test.mkv'
# )
#
# bsc_core.BscFfmpeg.extract_frame(
#     'Z:/temeporaries/dongchangbao/playblast_tool/test.export.v004.mov', 'Z:/temeporaries/dongchangbao/playblast_tool/test.export.v004.png', 0
# )

cmd_script = bsc_core.BscFfmpeg.generate_video_coding_convert_cmd_script(
    input='Z:/temporaries/camera_mask/maya_avi_1.avi', output='Z:/temporaries/camera_mask/maya_avi_1.mov',
    coding='MPEG4'
)

print cmd_script

bsc_core.BscProcess.execute_as_trace(cmd_script)
