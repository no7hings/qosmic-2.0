# coding:utf-8
import lxusd.core as usd_core

image_opt = usd_core.ImageOpt('/data/e/workspace/lynxi/test/maya/vertex-color/test.<udim>.jpg')

print image_opt.get_rgb_at_coord(1.5, 0.5)

