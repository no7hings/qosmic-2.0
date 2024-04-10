# coding:utf-8
import lxbasic.dcc.core as bsc_dcc_core

import lxbasic.dcc.objects as bsc_dcc_objects

from .. import abstracts as bsc_fnc_abstracts


class FncExporterForDotMaInfo(
    bsc_fnc_abstracts.AbsFncOptionBase
):
    OPTION = dict(
        file_path=None,
        root=None
    )

    def __init__(self, option):
        super(FncExporterForDotMaInfo, self).__init__(option)

    def execute(self):
        import os

        file_path = self.get('file_path')
        root = self.get('root')

        base, ext = os.path.splitext(file_path)
        r = bsc_dcc_core.DotMaOpt(file_path)
        _info = r.get_mesh_info(root=root)

        bsc_dcc_objects.StgYaml('{}.info.yml'.format(base)).set_write(_info)


class FncExporterForDotMa(
    bsc_fnc_abstracts.AbsFncOptionBase,
    bsc_fnc_abstracts.AbsFncForDotXgenDef
):
    OPTION = dict(
        file_path_src=None,
        file_path_tgt=None,
        root=None
    )

    def __init__(self, option):
        super(FncExporterForDotMa, self).__init__(option)

    def execute(self):
        file_path_src = self.get('file_path_src')
        file_path_tgt = self.get('file_path_tgt')

        bsc_dcc_objects.StgFile(file_path_src).copy_to_file(file_path_tgt)
        # copy xgen files
        self._copy_scene_xgen_collection_files_to(
            file_path_src,
            file_path_tgt
        )

