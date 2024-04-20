# coding:utf-8
import glob

import lxbasic.dcc.objects as bsc_dcc_objects

d_p = '/l/projects/m1/data/layout_exteral_assets/chr'

f_p_s = '/l/projects/m1/data/layout_exteral_assets/chr/{old_name}/rig/rig_layout/maya/scenes/{old_name}.rig.rig_layout.v???.ma'

f_p_t = '/l/prod/cgm/work/assets/chr/{new_name}/{step}/{task}/maya/scenes/{new_name}.{step}.{task}.v001.ma'

d = bsc_dcc_objects.StgDirectory(d_p)

lis = []

ms = []
ss = []
rs = []

for i in d.get_children():
    i_name = i.name
    i_new_name = 'ext_{}'.format(i_name.lower())
    lis.append(i_new_name)
    i_g_p = f_p_s.format(
        **dict(
            old_name=i_name
        )
    )
    _ = glob.glob(i_g_p)
    if _:
        _.sort()
        i_f_s = _[-1]
        for j_step, j_task in [
            ('mod', 'modeling'),
            ('rig', 'rigging'),
            ('srf', 'surfacing')
        ]:
            j_f_t = f_p_t.format(
                **dict(
                    new_name=i_new_name,
                    step=j_step,
                    task=j_task
                )
            )
            if j_step == 'mod':
                # print j_f_t
                ms.append(j_f_t)
            elif j_step == 'srf':
                # print j_f_t
                ss.append(j_f_t)
            elif j_step == 'rig':
                rs.append(j_f_t)
            # print i_f_s, j_f_t
            # bsc_dcc_objects.StgFile(
            #     i_f_s
            # ).copy_to_file(
            #     j_f_t
            # )

print rs
