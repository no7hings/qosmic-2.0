# coding:utf-8
import lxbasic.fnc.abstracts as bsc_fnc_abstracts
# katana
from ... import core as ktn_core
# katana dcc
from ...dcc import objects as ktn_dcc_objects

from ...dcc import operators as ktn_dcc_operators


class FncExporterForRenderTexture(
    bsc_fnc_abstracts.AbsFncExporterForDccTextureDef,
    bsc_fnc_abstracts.AbsFncOptionBase,
):
    FIX_NAME_BLANK = 'fix_name_blank'
    USE_TX = 'repath_to_target_force'
    WITH_REFERENCE = 'width_reference'
    OPTION = dict(
        directory_base='',
        directory='',
        location='',
        fix_name_blank=False,
        width_reference=False,
        use_environ_map=False,
        #
        copy_source=False,
    )

    def __init__(self, option=None):
        super(FncExporterForRenderTexture, self).__init__(option)
        self._directory_path_dst = self.get('directory')
        self._directory_path_base = self.get('directory_base')
        self._location = self.get('location')

    def execute(self):
        w_s = ktn_core.WorkspaceSetting()
        opt = w_s.get_current_look_output_opt_force()
        if opt is None:
            return

        s = ktn_dcc_operators.LookOutputOpt(opt)

        location = s.get_geometry_root()
        #
        texture_references = ktn_dcc_objects.TextureReferences()
        dcc_shaders = s.get_all_dcc_geometry_shaders_by_location(location)
        dcc_objs = texture_references.get_objs(
            include_paths=[i.path for i in dcc_shaders]
        )
        self.copy_and_repath_as_base_link_fnc(
            directory_path_bsc=self._directory_path_base, directory_path_dst=self._directory_path_dst,
            dcc_objs=dcc_objs,
            fix_name_blank=self.get('fix_name_blank'),
            with_reference=self.get('width_reference'),
            #
            ignore_missing_texture=True,
            remove_expression=True,
            use_environ_map=self.get('use_environ_map'),
            #
            repath_fnc=texture_references.repath_fnc,
            #
            copy_source=self.get('copy_source'),
        )
