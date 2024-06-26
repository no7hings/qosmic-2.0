# coding:utf-8
import collections
import re

import os


class MayaAscii(object):
    SEP = '\n'

    def __init__(self, file_path):
        self._file_path = file_path
        if os.path.isfile(self._file_path) is False:
            raise RuntimeError()

        self._load_lines()

    def _load_lines(self):
        self._lines = []
        if self._file_path is not None:
            with open(self._file_path) as f:
                data = f.read()
                sep = self.SEP
                self._lines = map(lambda x: r'{}{}'.format(x, sep), data.split(sep))

    def get_node_dict(self):
        dict_ = collections.OrderedDict()
        p_0 = r'createNode (.*) -s -n "(.*)";'+self.SEP
        p_1 = r'createNode (.*) -n "(.*)";'+self.SEP
        p_2 = r'(.*)" -p "(.*)'

        path_cur = None
        for i_idx, i_line in enumerate(self._lines):
            if re.search(p_0, i_line):
                continue

            i_r_0 = re.search(p_1, i_line)
            if i_r_0:
                i_node_type = i_r_0.group(1)
                i_s_1 = i_r_0.group(2)
                i_r_1 = re.search(p_2, i_s_1)
                if i_r_1:
                    i_node_name = i_r_1.group(1)
                    i_parent_name = i_r_1.group(2)
                else:
                    i_node_name = i_s_1
                    i_parent_name = None

                if i_parent_name is None:
                    i_node_path = '/{}'.format(i_node_name)
                else:
                    i_parent_path = path_cur
                    i_node_path = '{}/{}'.format(i_parent_path, i_node_name)

                path_cur = i_node_path
                dict_[i_node_path] = i_node_type

        return dict_

