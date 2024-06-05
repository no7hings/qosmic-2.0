# coding:utf-8
from __future__ import print_function

import os

import fnmatch

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgeneral.dcc.abstracts as gnl_dcc_abstracts


class AbsArnoldSetup(gnl_dcc_abstracts.AbsDccSetup):
    def __init__(self, root):
        super(AbsArnoldSetup, self).__init__(root)

    def add_procedurals(self, *args):
        [self.add_environ_fnc('ARNOLD_PROCEDURAL_PATH', i) for i in map(self._path_process_, args)]

    def add_plugins(self, *args):
        [self.add_environ_fnc('ARNOLD_PLUGIN_PATH', i) for i in map(self._path_process_, args)]

    def add_xgen(self, *args):
        [self.add_environ_fnc('XGEN_LOCATION', i) for i in map(self._path_process_, args)]

    def set_run(self):
        NotImplementedError()


class MtoaSetup(AbsArnoldSetup):
    def __init__(self, root):
        super(MtoaSetup, self).__init__(root)

    def set_run(self):
        self.add_pythons('{root}/scripts')
        self.add_libraries('{root}/bin')
        self.add_procedurals('{root}/procedurals')
        self.add_plugins('{root}/plugins', '{root}/procedurals')
        self.add_bin_fnc('{root}/bin')


class KtoaSetup(AbsArnoldSetup):
    def __init__(self, root):
        super(KtoaSetup, self).__init__(root)

    def set_run(self):
        pass


class MayaSetup(object):
    def __init__(self):
        pass

    @classmethod
    def _set_maya_ae_setup_(cls):
        from lxmaya.node_template import startup as mya_node_template_startup

        _ = bsc_core.EnvBaseMtd.get_as_array(
            'QSM_MAYA_ARNOLD_RESOURCES'
        )
        lis = []
        for i in _:
            path_opt = bsc_storage.StgPathOpt(i)
            if path_opt.get_is_exists() is True:
                i_ae_path = '{}/ae'.format(path_opt.get_path())
                if bsc_storage.StgPathOpt(i_ae_path).get_is_exists() is True:
                    lis.append(i_ae_path)
        #
        if lis:
            mya_node_template_startup.setup_node_template_prcs(
                lis
            )
            bsc_log.Log.trace_method_result(
                'maya-ae setup',
                'path="{}"'.format(', '.join(lis))
            )

    @classmethod
    def run(cls):
        raw = os.environ.get('MAYA_PLUG_IN_PATH')
        if raw:
            paths = raw.split(os.pathsep)
            if paths:
                match_pattern = '*/mtoa/*/plug-ins'
                results = fnmatch.filter(paths, match_pattern)
                if results:
                    mtoa_plugin_path = results[0]
                    MtoaSetup(mtoa_plugin_path).set_run()
        #
        if bsc_core.BasApplication.get_is_maya():
            cls._set_maya_ae_setup_()
