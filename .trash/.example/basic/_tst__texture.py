# coding:utf-8
import lxgeneral.dcc.objects as gnl_dcc_objects

print gnl_dcc_objects.StgTexture._generate_unit_jpg_create_cmd(
    '/production/library/resource/all/hdri/modern_buildings_2_4k/v0001/hdri/original/src/modern_buildings_2_4k.exr',
    '/production/library/resource/all/hdri/modern_buildings_2_4k/v0001/hdri/original/jpg/modern_buildings_2_4k.jpg'
)
