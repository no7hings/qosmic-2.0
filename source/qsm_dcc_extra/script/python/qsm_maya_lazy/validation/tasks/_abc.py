# coding:utf-8
import pkgutil

import importlib

import lxbasic.log as bsc_log

import lxbasic.content as bsc_content

import qsm_lazy.validation.core as qsm_lzy_vld_core

import qsm_maya.core as qsm_mya_core


class AbsValidationTask(object):
    TEST_FLAG = False

    LOG_KEY = None

    OPTION_KEY = None

    @classmethod
    def get_prc_cls(cls, branch, leaf):
        module_name = 'qsm_maya_lazy.validation.prc.{}.{}'.format(branch, leaf)
        _ = pkgutil.find_loader(module_name)
        if _:
            module = importlib.import_module(module_name)
            return module.__dict__.get('Main')

    def __init__(self, namespace):
        self._namespace = namespace
        self._file_path = qsm_mya_core.ReferenceNamespacesCache().get_file(namespace)

        self._validation_options = qsm_lzy_vld_core.DccValidationOptions(self.OPTION_KEY)

        self._result_content = bsc_content.Dict()

        self._kwargs = dict(
            task=self,
            namespace=self._namespace,
            result_content=self._result_content,
            validation_options=self._validation_options
        )

    def branch_prc(self, branch, leafs):
        for i_leaf in leafs:
            i_prc_cls = self.get_prc_cls(branch, i_leaf)
            if i_prc_cls:
                i_prc_cls.BRANCH = branch
                i_prc_cls.LEAF = i_leaf
                i_prc = i_prc_cls(
                    **self._kwargs
                )
                i_prc.execute()
            else:
                bsc_log.Log.trace_method_error(
                    self.LOG_KEY, 'process: {}.{} is not found'.format(branch, i_leaf)
                )
