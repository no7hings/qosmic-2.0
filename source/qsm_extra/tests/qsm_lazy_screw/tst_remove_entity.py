# coding:utf-8
import qsm_lazy.screw.core as c

scr_stage = c.Stage('asset_test')

# scr_stage.create_tag_assign(
#     '/amanda', '/mesh_count/face/unspecified'
# )

scr_stage.remove_assign(
'/amanda', '/mesh_count/face/unspecified'
)