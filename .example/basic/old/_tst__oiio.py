# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

f_i = '/production/library/resource/all/imperfection/rain_drops_and_streaks_001/v0001/image/preview.png'

_, cmd = bsc_storage.ImgOiioOptForThumbnail(
    f_i
).get_thumbnail_jpg_create_args_with_background_over(
    width=256, background_rgba=(71, 71, 71, 255)
)

if cmd:
    bsc_core.PrcBaseMtd.execute_with_result(
        cmd
    )
