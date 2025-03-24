# coding:utf-8
import re

from ...core import path as _scn_cor_path


class CEL(object):

    @classmethod
    def _to_args(cls, s):
        # '/root/maya/scene//*{attr("type")=="MaysScene"}'
        # noinspection RegExpRedundantEscape
        parts = re.split(r'\{(.*?)\}', s, maxsplit=1)
        s_0 = parts[0]  # '/root/world/geo/master//*'
        s_1 = parts[1] if len(parts) > 1 else ''  # attr("type")=="MaysScene"
        return s_0, s_1

    def __init__(self, stage, s):
        self._stage = stage
        self._ptn, self._exp = self._to_args(s)

    @property
    def pattern(self):
        return self._ptn

    @property
    def expression(self):
        return self._exp

    def fetchall(self):
        list_ = []
        node_paths = _scn_cor_path.Selection.fetchall(self._stage.get_node_paths(), self._ptn)
        for i in node_paths:
            i_node = self._stage.get_node(i)
            if i_node.match_exp(self._exp):
                list_.append(i_node)
        return list_
