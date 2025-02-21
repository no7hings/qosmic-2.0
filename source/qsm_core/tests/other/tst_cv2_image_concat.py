# coding:utf-8
import lxbasic.storage as bsc_storage

import lxbasic.cv.core as bsc_cv_core

bsc_cv_core.VideoConcat(
    bsc_storage.StgFileTiles.get_tiles(
        'C:/Users/nothings/.qosmic/temporary/2024_0628/EEAB9B0F-3534-11EF-A0A2-4074E0DA267B/image.####.jpg'
    ),
    'C:/Users/nothings/.qosmic/temporary/2024_0628/EEAB9B0F-3534-11EF-A0A2-4074E0DA267B/opendv-output.30.mov',
    fps=30
).execute()
