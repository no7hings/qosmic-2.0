# coding:utf-8
import lxbasic.core as bsc_core

c = 'Y:/deploy/rez-packages/external/ffmpeg/7.0.1/platform-windows/bin/ffmpeg.exe -f concat -safe 0 -r 30 -i "C:/Users/nothings/.qosmic/temporary/2024_0628/EEAB9B0F-3534-11EF-A0A2-4074E0DA267B/image.1-150.files" -vf "fps=30" -c:v mpeg4 -pix_fmt yuv420p -b:v 8000k -y "C:/Users/nothings/.qosmic/temporary/2024_0628/EEAB9B0F-3534-11EF-A0A2-4074E0DA267B/ffmpeg-output-2.30.mov"'

bsc_core.BscProcess.execute_as_trace(
    c
)

# print bsc_core.BscFfmpeg.get_frame_count(
#     'C:/Users/nothings/.qosmic/temporary/2024_0628/EEAB9B0F-3534-11EF-A0A2-4074E0DA267B/ffmpeg-output.24.mov'
# )