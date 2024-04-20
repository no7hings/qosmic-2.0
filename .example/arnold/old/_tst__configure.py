# coding:utf-8
import lxbasic.texture as bsc_texture

# c = bsc_texture.TxrMethodForColorSpaceAsTxConvert.generate_instance()
#
# print c.get_name_patterns()
#
# print c.get_color_space_mapper()
#
# print c.get_tx_color_space_input('/production/library/resource/all/surface/mossy_ground_umkkfcolw/v0001/texture/acescg/src/mossy_ground_umkkfcolw.albedo.exr')
#
# c = bsc_texture.TxrMethodForColorSpaceAsAces.generate_instance()
#
# print c.get_ocio_file()

m = bsc_texture.TxrMethodForBuild.generate_instance()

for i in [
    '/data/e/workspace/lynxi/test/texture/mossy_ground_umkkfcolw.albedo.1001.0001.tx',
    '/data/e/workspace/lynxi/test/texture/mossy_ground_umkkfcolw.albedo.1001.0001.tx',
    '/data/e/workspace/lynxi/test/texture/mossy_ground_umkkfcolw.albedo.1001.tx',
    '/data/e/workspace/lynxi/test/texture/mossy_ground_umkkfcolw.albedo.tx'
]:
    print m.generate_all_texture_args(
        i
    )

