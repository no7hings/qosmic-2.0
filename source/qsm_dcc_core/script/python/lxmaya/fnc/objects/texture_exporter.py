# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.fnc.abstracts as bsc_fnc_abstracts
# maya
from ...core.wrap import *

from ... import core as mya_core
# maya dcc
from ...dcc import objects as mya_dcc_objects

from ...dcc import operators as mya_dcc_operators


class FncExporterForRenderTexture(
    bsc_fnc_abstracts.AbsFncExporterForDccTextureDef,
    bsc_fnc_abstracts.AbsFncOptionBase,
):
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
    PLUGINS = [
        'mtoa'
    ]

    def __init__(self, option=None):
        super(FncExporterForRenderTexture, self).__init__(option)
        self._directory_path_base = self.get('directory_base')
        self._directory_path_dst = self.get('directory')
        self._location = self.get('location')

    def execute(self):
        for i in self.PLUGINS:
            cmds.loadPlugin(i, quiet=1)
        #
        root_dag_path = bsc_core.PthNodeOpt(self._location)
        root_mya_dag_path = root_dag_path.translate_to(
            pathsep=mya_core.MyaUtil.OBJ_PATHSEP
        )
        #
        root_mya_obj = mya_dcc_objects.Group(root_mya_dag_path.path)
        if root_mya_obj.get_is_exists() is True:
            dcc_geometries = root_mya_obj.get_descendants()
            #
            objs_look_opt = mya_dcc_operators.ObjsLookOpt(dcc_geometries)
            includes = objs_look_opt.get_texture_reference_paths()
            if includes:
                texture_references = mya_dcc_objects.TextureReferences
                #
                self.copy_and_repath_as_base_link_fnc(
                    directory_path_bsc=self._directory_path_base, directory_path_dst=self._directory_path_dst,
                    dcc_objs=texture_references._get_objs_(includes),
                    #
                    fix_name_blank=self.get('fix_name_blank'),
                    with_reference=self.get('width_reference'),
                    #
                    ignore_missing_texture=True,
                    use_environ_map=self.get('use_environ_map'),
                    #
                    repath_fnc=texture_references.repath_fnc,
                    #
                    copy_source=self.get('copy_source'),
                )


class FncGeneralTextureExporter(
    bsc_fnc_abstracts.AbsFncExporterForDccTextureDef,
    bsc_fnc_abstracts.AbsFncOptionBase
):
    OPTION = dict(
        directory='',
        location='',
        fix_name_blank=False,
        width_reference=False,
        use_environ_map=False,
        ignore_missing_texture=False,
        #
        copy_source=False
    )
    PLUGINS = [
        'mtoa'
    ]

    def __init__(self, option):
        super(FncGeneralTextureExporter, self).__init__(option)

    def execute(self):
        for i in self.PLUGINS:
            cmds.loadPlugin(i, quiet=1)
        #
        dcc_objs = mya_dcc_objects.TextureReferences().get_objs()
        texture_references = mya_dcc_objects.TextureReferences
        #
        self.copy_and_repath_fnc(
            directory_path_dst=self.get('directory'),
            dcc_objs=dcc_objs,
            #
            fix_name_blank=self.get('fix_name_blank'),
            with_reference=self.get('width_reference'),
            #
            ignore_missing_texture=self.get('ignore_missing_texture'),
            use_environ_map=self.get('use_environ_map'),
            #
            repath_fnc=texture_references.repath_fnc,
            copy_source=self.get('copy_source'),
        )
