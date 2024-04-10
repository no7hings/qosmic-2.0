# coding:utf-8
import lxresource as bsc_resource

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from .. import objects as bsc_dcc_objects


class ScpOslBuilder(object):
    """
import lxarnold.startup as and_startup

and_startup.MtoaSetup('/job/PLE/bundle/thirdparty/arnold/6.1.0.1/Linux').set_run()

d_p = '/data/f/osl'

import lxbasic.dcc.scripts as bsc_scripts

bsc_scripts.ScpOslBuilder(
    d_p
).do_compile()

bsc_scripts.ScpOslBuilder(
    d_p
).do_create_ui_template()
    """
    @classmethod
    def generate_katana_ui_template(cls, file_path, file_path_output):
        output_file_opt = bsc_storage.StgFileOpt(file_path_output)
        output_file_opt.create_directory()
        info = bsc_storage.OslFileMtd.get_info(file_path)
        if info:
            j2_template = bsc_resource.RscExtendJinja.get_template('arnold/katana-ui-template-v002')
            raw = j2_template.render(
                **info
            )

            output_file_opt.set_write(raw)

    @classmethod
    def generate_maya_ui_template(cls, file_path, file_path_output):
        output_file_opt = bsc_storage.StgFileOpt(file_path_output)
        output_file_opt.create_directory()
        info = bsc_storage.OslFileMtd.get_info(file_path)
        if info:
            j2_template = bsc_resource.RscExtendJinja.get_template('arnold/maya-ui-template-v002')
            raw = j2_template.render(
                **info
            )

            output_file_opt.set_write(raw)

    def __init__(self, directory_path):
        self._directory_path = directory_path

    def do_compile(self):
        d = bsc_dcc_objects.StgDirectory(self._directory_path)

        for i_f_p in d.get_child_file_paths():
            i_f = bsc_dcc_objects.StgFile(i_f_p)
            if i_f.ext == '.osl':
                bsc_storage.OslFileMtd.compile(
                    i_f.path
                )

    def do_create_ui_template(self):
        d = bsc_dcc_objects.StgDirectory(self._directory_path)

        for i_f_p in d.get_child_file_paths():
            i_f = bsc_dcc_objects.StgFile(i_f_p)
            if i_f.ext == '.osl':
                i_katana_o_f_p = '{}/Args/{}.args'.format(d.path, i_f.name_base)
                self.generate_katana_ui_template(
                    i_f.path, i_katana_o_f_p
                )
                i_maya_o_f_p = '{}/maya/ae/ae_{}.py'.format(d.get_parent().path, i_f.name_base)
                self.generate_maya_ui_template(
                    i_f.path, i_maya_o_f_p
                )
