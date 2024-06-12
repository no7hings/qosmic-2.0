# coding:utf-8
import lxbasic.media.core as bsc_mda_core

# o = bsc_mda_core.VideoCaptureOpt('F:/video/film/Blonde[金发梦露](2022)/Blonde.2022.1080p.NF.WEB-DL.DDP5.1.Atmos.HDR.H.265-PTerWEB.mkv')
#
# o.create_thumbnail(
#     'Z:/temeporaries/dongchangbao/snapshot/test.png'
# )
#
# o.release()

bsc_mda_core.FrameExtractor(
'Z:/temeporaries/dongchangbao/playblast_tool/test.export.v004.mov',
'Z:/temeporaries/dongchangbao/playblast_tool/test.export.v004.png'
).run()
