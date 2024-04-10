# coding:utf-8
import re
# katana
from ..core.wrap import *

from .. import core as ktn_core


# noinspection PyUnusedLocal
class ScpLookAssignsReplace(object):
    DCC_TYPES_INCLUDE = [
        'MaterialAssign',
        'ArnoldObjectSettings',
    ]

    def __init__(self, string_src, string_tgt):
        self._string_src = string_src
        self._string_tgt = string_tgt

    @classmethod
    def _get_ktn_objs_(cls, obj_type_names):
        return [j for i in obj_type_names for j in NodegraphAPI.GetAllNodesByType(i) or []]

    @classmethod
    def _get_values_(cls, p):
        ptn = '[(](.*?)[)]'
        value = p.getValue(0)
        print value
        if value:
            _ = re.findall(ptn, value)
            if _:
                return _[0].split(' ')
            else:
                return [value]

    @classmethod
    def _set_values_(cls, p, values):
        if values:
            if len(values) == 1:
                value = values[0]
            else:
                value = '({})'.format(' '.join(values))
            print value
            # p.setValue(value, 0)

    @ktn_core.Modifier.undo_debug_run
    def set_run(self):
        for i in self._get_ktn_objs_(self.DCC_TYPES_INCLUDE):
            i_p = i.getParameter('CEL')
            if i_p.isExpression() is False:
                i_value_src = i_p.getValue(0)
                i_value_tgt = i_value_src.replace(
                    self._string_src, self._string_tgt
                )
                i_p.setValue(i_value_tgt, 0)
