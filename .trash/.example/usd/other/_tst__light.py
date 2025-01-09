# coding:utf-8

from lxusd.core import *

stage = Usd.Stage.CreateInMemory()

light_xform_prim = stage.DefinePrim('/test_light', 'Xform')
light_prim = stage.DefinePrim('/test_light/test_light_shape', 'SphereLight')
light = UsdLux.SphereLight(light_prim)
light.CreateIntensityAttr().Set(5)
light.CreateExposureAttr().Set(1.0)
light.CreateRadiusAttr().Set(1.0)
#
shaping_api = UsdLux.ShapingAPI(light_prim)
shaping_api.CreateShapingFocusAttr().Set(2.0)
UsdGeom.Xformable(light_xform_prim).MakeMatrixXform().Set(
    Gf.Matrix4d(((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (100, 100, 100, 1)))
)

stage.Export(
    '/data/e/myworkspace/td/lynxi/script/python/lxusd/.etc/sphere_light.usda'
)
