# coding:utf-8
import lxresource as bsc_resource

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.dcc.core as bsc_dcc_core

from .. import abstracts as bsc_fnc_abstracts


class FncExporterForDotXarc(
    bsc_fnc_abstracts.AbsFncOptionBase
):
    OPTION = dict(
        file='',
        name='',
        jpg_file='',
        color=[],
        gpu_files=[],
        ass_files=[]
    )

    def __init__(self, option=None):
        super(FncExporterForDotXarc, self).__init__(option)

    @classmethod
    def _update_option_fnc(cls, option, include_keys):
        def convert_fnc_(path_):
            return bsc_storage.StgEnvPathMapper.map_to_env(
                path_, pattern='${KEY}'
            )

        for i_k, i_v in option.items():
            if i_k in include_keys:
                if isinstance(i_v, (tuple, list)):
                    for j_seq, j in enumerate(i_v):
                        i_v[j_seq] = convert_fnc_(j)
                else:
                    option[i_k] = convert_fnc_(i_v)

    def set_run(self):
        option = self.get_option()
        #
        self._update_option_fnc(option, ['jpg_file', 'gpu_files', 'ass_files'])
        #
        file_path = option.get('file')
        #
        j2_template = bsc_resource.RscExtendJinja.get_template('xarc/proxy')
        raw = j2_template.render(
            **self._option
        )

        bsc_storage.StgFileOpt(file_path).set_write(
            raw
        )

        bsc_log.Log.trace_method_result(
            'dot-xarc-export',
            'file="{}"'.format(file_path)
        )


class FncExporterForDotXgen(
    bsc_fnc_abstracts.AbsFncOptionBase,
    bsc_fnc_abstracts.AbsFncForDotXgenDef
):
    OPTION = dict(
        # etc. {directory}/{scene}__{xgen}.xgen
        xgen_collection_file='',
        # etc. {directory}/scenes
        xgen_project_directory='',
        # etc. {directory}/xgen/collections
        xgen_collection_directory='',
        # etc. {xgen}_description
        xgen_collection_name='',
    )

    def __init__(self, option):
        super(FncExporterForDotXgen, self).__init__(option)

    def set_run(self):
        option_opt = self.get_option()
        #
        xgen_collection_file_path = option_opt.get('xgen_collection_file')
        xgen_project_directory_path_tgt = option_opt.get('xgen_project_directory')
        xgen_collection_directory_path_tgt = option_opt.get('xgen_collection_directory')
        xgen_collection_name = option_opt.get('xgen_collection_name')
        #
        self._repath_xgen_collection_file_to(
            xgen_collection_file_path,
            xgen_project_directory_path_tgt,
            xgen_collection_directory_path_tgt,
            xgen_collection_name,
        )


class FncExporterForDotXgenUsda(
    bsc_fnc_abstracts.AbsFncOptionBase,
    bsc_fnc_abstracts.AbsFncForDotXgenDef
):
    OPTION = dict(
        file='',
        location='',
        maya_scene_file='',
    )

    def __init__(self, option=None):
        super(FncExporterForDotXgenUsda, self).__init__(option)

    def set_run(self):
        option_opt = self.get_option()
        file_path = option_opt.get('file')
        location = option_opt.get('location')
        location_dag_opt = bsc_core.PthNodeOpt(location)
        maya_scene_file_path = option_opt.get('maya_scene_file')
        if maya_scene_file_path:
            xgen_collection_file_paths = self._find_scene_xgen_collection_file_paths(maya_scene_file_path)
            key = 'usda/asset-xgen'
            t = bsc_resource.RscExtendJinja.get_template(
                key
            )

            c = bsc_resource.RscExtendJinja.get_configure(
                key
            )
            for i_xgen_collection_file_path in xgen_collection_file_paths:
                i_xgen_collection_name = self._get_xgen_collection_name(
                    i_xgen_collection_file_path
                )
                i_dot_xgen_file_reader = bsc_dcc_core.DotXgenOpt(
                    i_xgen_collection_file_path
                )
                i_xgen_description_properties = i_dot_xgen_file_reader.get_description_properties()
                i_description_names = i_xgen_description_properties.get_top_keys()
                #
                c.set(
                    'asset.xgen.collections.{}.file'.format(i_xgen_collection_name),
                    bsc_storage.StgPathMtd.get_file_realpath(
                        file_path, i_xgen_collection_file_path
                    )
                )
                c.set(
                    'asset.xgen.collections.{}.description_names'.format(i_xgen_collection_name),
                    i_description_names
                )

            c.do_flatten()
            raw = t.render(
                c.value
            )

            bsc_storage.StgFileOpt(file_path).set_write(raw)


if __name__ == '__main__':
    FncExporterForDotXarc(
        option={
            'jpg_file': '/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/jpg/default.jpg',
            'name': 'ast_shl_cao_a_static',
            'color': [1, 1, 1],
            'file': '/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/xarc/default/static.xarc',
            'gpu_files': [
                '/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/gpu/default/static.abc',
                '/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/gpu/default/static.lod01.abc',
                '/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/gpu/default/static.lod02.abc'
            ],
            'ass_files': [
                '/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/ass/default/static.ass',
                '/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/ass/default/static.lod01.ass',
                '/l/prod/cjd/publish/assets/flg/ast_shl_cao_a/srf/surfacing/ast_shl_cao_a.srf.surfacing.v002/proxy/ass/default/static.lod02.ass'
            ]
        }

    ).set_run()
