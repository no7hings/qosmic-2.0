# coding:utf-8
import re
import sys

# noinspection PyUnresolvedReferences
import maya.cmds as cmds

from ... import core as _mya_core


class ReferenceFix(object):
    def __init__(self, reference_node):

        self._reference_node = reference_node

        self._namespace = _mya_core.Reference.get_namespace(self._reference_node)

    @staticmethod
    def _get_anm_curve_args(input_str):
        match = re.match(r"^(.*)_([a-zA-Z]+)(\d*)$", input_str)
        if match:
            return match.group(1), match.group(2)

    def find_one_control(self, control_key):
        _ = cmds.ls('{}:{}'.format(self._namespace, control_key), long=1)
        if _:
            return _[0]

    def fix_placeholder(self):
        reference_node = self._reference_node
        if reference_node:
            indices = _mya_core.NodeAttribute.get_array_indices(reference_node, 'placeHolderList')
            for i_index in indices:
                i_source = _mya_core.NodeAttribute.get_source(reference_node, 'placeHolderList[{}]'.format(i_index))
                if not i_source:
                    continue

                i_node = i_source.split('.')[0]
                i_args = self._get_anm_curve_args(i_node)
                if i_args:
                    i_control_key, i_atr_name = i_args
                    i_control = self.find_one_control(i_control_key)
                    if i_control:
                        if _mya_core.NodeAttribute.is_exists(i_control, i_atr_name) is True:
                            if _mya_core.NodeAttribute.is_settable(i_control, i_atr_name):
                                _mya_core.Connection.create(
                                    i_source, '{}.{}'.format(i_control, i_atr_name)
                                )
                else:
                    sys.stderr.write(
                        'Unavailable node: {}\n'.format(i_node)
                    )
