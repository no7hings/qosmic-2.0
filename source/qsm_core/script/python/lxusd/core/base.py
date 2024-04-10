# coding:utf-8
import six

import lxuniverse.core as unr_core
# usd
from .wrap import *

from . import configure as usd_cor_configure


class UsdTypeMtd(object):
    @classmethod
    def get(cls, key):
        if key in usd_cor_configure.UsdTypes.MAPPER:
            return usd_cor_configure.UsdTypes.MAPPER[key]


class UsdPrimQuery(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim


class UsdStapeOpt(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim
        self._usd_fnc = UsdGeom.Imageable(self._usd_prim)

    def get_is_visible(self):
        p = self._usd_fnc.GetVisibilityAttr()
        if p:
            return p.Get() != UsdGeom.Tokens.invisible
        return True

    def set_visible(self, boolean):
        if boolean is True:
            self._usd_fnc.MakeVisible()
        else:
            self._usd_fnc.MakeInvisible()

    def swap_visibility(self):
        self.set_visible(
            not self.get_is_visible()
        )

    def get_primvar(self, key):
        if self._usd_fnc.HasPrimvar(key) is True:
            return self._usd_fnc.GetPrimvar(key).Get()


class UsdShaderOpt(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim
        self._usd_fnc = UsdShade.Shader(self._usd_prim)

    def set_file(self, file_path):
        _ = self._usd_fnc.GetInput('file')
        if _ is None:
            _ = self._usd_fnc.CreateInput('file', Sdf.ValueTypeNames.Asset)
        _.Set(file_path)

    def set_metallic(self, value):
        _ = self._usd_fnc.GetInput('metallic')
        if _ is None:
            _ = self._usd_fnc.CreateInput('metallic', Sdf.ValueTypeNames.Float)
        _.Set(value)

    def set_ior(self, value):
        _ = self._usd_fnc.GetInput('ior')
        if _ is None:
            _ = self._usd_fnc.CreateInput('ior', Sdf.ValueTypeNames.Float)
        _.Set(value)

    def set_as_float(self, key, value):
        _ = self._usd_fnc.GetInput(key)
        if _ is None:
            _ = self._usd_fnc.CreateInput(key, Sdf.ValueTypeNames.Float)
        _.Set(value)

    def set_as_rgb(self, key, value):
        _ = self._usd_fnc.GetInput(key)
        if _ is None:
            _ = self._usd_fnc.CreateInput(key, Sdf.ValueTypeNames.Color3f)
        _.Set(value)

    def disconnect_input_at(self, key):
        _ = self._usd_fnc.GetInput(key)
        if _ is not None:
            if _.HasConnectedSource() is True:
                _.DisconnectSource()

    def set_as_float3(self, key, value):
        _ = self._usd_fnc.GetInput(key)
        if _ is None:
            _ = self._usd_fnc.CreateInput(key, Sdf.ValueTypeNames.Float3)
        _.Set(value)

    def set_as_float4(self, key, value):
        _ = self._usd_fnc.GetInput(key)
        if _ is None:
            _ = self._usd_fnc.CreateInput(key, Sdf.ValueTypeNames.Float4)
        _.Set(value)

    def set_as_asset(self, key, value):
        _ = self._usd_fnc.GetInput(key)
        if _ is None:
            _ = self._usd_fnc.CreateInput(key, Sdf.ValueTypeNames.Asset)
        #
        _.Set(value)


class UsdMaterialAssignOpt(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim

    def assign(self, *args):
        arg = args[0]
        r = self._usd_prim.CreateRelationship('material:binding')
        r.BlockTargets()
        if isinstance(arg, six.string_types):
            r.AddTarget(
                self._usd_prim.GetStage().GetPrimAtPath(arg).GetPath()
            )
        elif isinstance(arg, Sdf.Path):
            r.AddTarget(
                arg
            )
        elif isinstance(arg, Usd.Prim):
            r.AddTarget(
                arg.GetPath()
            )


class UsdXformOpt(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim
        self._usd_fnc = UsdGeom.Xform(self._usd_prim)

    def set_translate(self, x, y, z):
        pass

    def set_matrix(self, matrix):
        op = self._usd_fnc.MakeMatrixXform()
        op.Set(Gf.Matrix4d(matrix))

    def set_visible(self, boolean):
        if boolean is True:
            self._usd_fnc.MakeVisible()
        else:
            self._usd_fnc.MakeInvisible()


class UsdArnoldGeometryPropertiesOpt(object):
    PROPERTIES_TYPE_MAPPER = dict(
        opaque=unr_core.UnrType.CONSTANT_BOOLEAN,
        matte=unr_core.UnrType.CONSTANT_BOOLEAN,
        # visibility
        self_shadows=unr_core.UnrType.CONSTANT_BOOLEAN,
        # export
        sss_setname=None,
        trace_sets=None,
        # volume
        step_size=unr_core.UnrType.CONSTANT_FLOAT,
        volume_padding=unr_core.UnrType.CONSTANT_FLOAT,
        smoothing=unr_core.UnrType.CONSTANT_BOOLEAN,
        # mesh-subdiv
        subdiv_type=unr_core.UnrType.CONSTANT_STRING,
        subdiv_iterations=unr_core.UnrType.CONSTANT_INTEGER,
        subdiv_adaptive_error=unr_core.UnrType.CONSTANT_FLOAT,
        subdiv_adaptive_metric=unr_core.UnrType.CONSTANT_STRING,
        subdiv_adaptive_space=unr_core.UnrType.CONSTANT_STRING,
        subdiv_uv_smoothing=unr_core.UnrType.CONSTANT_STRING,
        subdiv_smooth_derivs=unr_core.UnrType.CONSTANT_BOOLEAN,
        subdiv_frustum_ignore=unr_core.UnrType.CONSTANT_BOOLEAN,
        # mesh-displacement
        disp_height=unr_core.UnrType.CONSTANT_FLOAT,
        disp_padding=unr_core.UnrType.CONSTANT_FLOAT,
        disp_zero_value=unr_core.UnrType.CONSTANT_FLOAT,
        disp_autobump=unr_core.UnrType.CONSTANT_BOOLEAN,
        # curve
        mode=unr_core.UnrType.CONSTANT_STRING,
        min_pixel_width=unr_core.UnrType.CONSTANT_FLOAT,
    )
    VISIBILITY_MAPPER = dict(

    )

    def __init__(self, usd_prim):
        self._usd_prim = usd_prim
        self._usd_fnc = UsdGeom.Imageable(self._usd_prim)
        self._usd_fnc = UsdGeom.Mesh(self._usd_prim)

    def set_properties(self, data):
        for k, v in data.items():
            self.set_property(k, v)

        # self._usd_fnc.CreateSubdivisionSchemeAttr(
        #     UsdGeom.Tokens.catmullClark
        # )

    def set_property(self, key, value):
        if key in self.PROPERTIES_TYPE_MAPPER:
            path = 'arnold:{}'.format(key)
            if self._usd_fnc.HasPrimvar(path) is False:
                p = self._usd_fnc.CreatePrimvar(
                    path,
                    UsdTypeMtd.get(
                        self.PROPERTIES_TYPE_MAPPER[key]
                    )
                )
            else:
                p = self._usd_fnc.GetPrimvar(
                    path
                )
            p.Set(value)


class UsdLightOpt(object):
    def __init__(self, usd_prim):
        self._usd_prim = usd_prim
        self._shaping_api = UsdLux.ShapingAPI(self._usd_prim)
        self._shadow_api = UsdLux.ShadowAPI(self._usd_prim)

    def set_shadow_enable(self, boolean):
        self._shadow_api.CreateShadowEnableAttr().Set(boolean)
        self._shadow_api.CreateShadowColorAttr().Set((1.0, 0.0, 0.0))

    def set_texture_file(self, value):
        usd_fnc = UsdLux.DomeLight(self._usd_prim)
        p = usd_fnc.GetTextureFileAttr()
        if not p:
            p = usd_fnc.CreateTextureFileAttr()
        p.Set(value)
