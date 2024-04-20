# coding:utf-8
import lxbasic.dcc.objects as bsc_dcc_objects

import lxbasic.shotgun as bsc_shotgun


for i_look_pass in ['default', 'C2', 'C3', 'C4', 'C5']:

    f = '/l/prod/cjd/publish/assets/chr/qunzhongnv_b/srf/surfacing/qunzhongnv_b.srf.surfacing.v014/render/katana/output/{}/primary.####.exr'.format(
        i_look_pass
    )

    bsc_shotgun.ImgOiioOptForThumbnail(
        bsc_dcc_objects.StgFile(f)
    ).convert_to(
        output_file_path='/l/prod/cjd/publish/assets/chr/qunzhongnv_b/srf/surfacing/qunzhongnv_b.srf.surfacing.v014/render/katana/output/{}.mov'.format(
            i_look_pass
        ),
        color_space='ACES CG'
    )
