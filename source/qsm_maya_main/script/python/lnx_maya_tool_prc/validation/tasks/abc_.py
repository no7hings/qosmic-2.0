# coding:utf-8
import pkgutil

import importlib

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.content as bsc_content

import lxbasic.resource as bsc_resource

import lnx_dcc_tool_prc.validation.core as lzy_vld_core

import qsm_maya.core as qsm_mya_core


class AbsValidationTask(object):
    TEST_FLAG = False

    LOG_KEY = None

    OPTION_KEY = None

    def __init__(self, namespace):
        self._namespace = namespace
        self._file_path = qsm_mya_core.ReferencesCache().get_file(namespace)

        self._validation_options = lzy_vld_core.DccValidationOptions(self.OPTION_KEY)

        self._result_content = bsc_content.Dict()

        self._kwargs = dict(
            task=self,
            namespace=self._namespace,
            result_content=self._result_content,
            validation_options=self._validation_options
        )

    def execute_branch_task_prc_for(self, branch, leafs, task_prc_cls):
        for i_leaf in leafs:
            self.execute_leaf_task_prc_for(branch, i_leaf, task_prc_cls)

    def execute_leaf_task_prc_for(self, branch, leaf, task_prc_cls):
        python_script_path = bsc_resource.BscResource.get(
            'scripts/validation_prc/maya/{}/{}.py'.format(branch, leaf)
        )
        if python_script_path:
            task_prc_cls.BRANCH = branch
            task_prc_cls.LEAF = leaf
            task_prc = task_prc_cls(**self._kwargs)
            bsc_core.BscScriptExecute.execute_python_file(
                file_path=python_script_path, task_prc=task_prc
            )
        else:
            bsc_log.Log.trace_method_error(
                self.LOG_KEY, 'process: {}.{} is not found'.format(branch, leaf)
            )
