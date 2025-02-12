# coding:utf-8
import collections

import re

from datetime import datetime

import lxbasic.core as bsc_core

from ..core import dcc_base as _dcc_base

from . import abc_


class MayaAscii(abc_.AbsDotfile):
    SEP = ';\n'

    def __init__(self, *args, **kwargs):
        super(MayaAscii, self).__init__(*args, **kwargs)

    def get_node_dict(self):
        # todo: add a check pattern
        dict_ = collections.OrderedDict()
        p_end = r'connectAttr.*'

        p_0 = r'createNode.*'

        p_1 = r'createNode (.*?) -s -n "(.*?)"'+self.SEP
        p_2 = r'createNode (.*?) -n "(.*?)"'+self.SEP
        p_3 = r'(.*?)" -p "(.*?)'

        path_cur = None
        for i_idx, i_line in enumerate(self._lines):
            if re.match(p_end, i_line, re.DOTALL):
                break

            if re.match(p_0, i_line, re.DOTALL):
                # ignore shared node
                if re.match(p_1, i_line, re.DOTALL):
                    continue

                i_r_2 = re.search(p_2, i_line)
                if i_r_2:
                    i_node_type = i_r_2.group(1)
                    i_s_1 = i_r_2.group(2)
                    i_r_3 = re.search(p_3, i_s_1)
                    if i_r_3:
                        i_node_name = i_r_3.group(1)
                        i_parent_name = i_r_3.group(2)
                    else:
                        i_node_name = i_s_1
                        i_parent_name = None

                    if i_parent_name is None:
                        i_node_path = '/{}'.format(i_node_name)
                    else:
                        i_parent_path = path_cur
                        i_node_path = '{}/{}'.format(i_parent_path, i_node_name)

                    path_cur = i_node_path
                    dict_[i_node_path] = dict(
                        type=i_node_type
                    )

        return dict_

    def get_nodes(self):
        list_ = []
        for k, v in self.get_node_dict().items():
            i_obj = bsc_core.BscNodePathOpt(k)
            i_obj.set_properties(v)
            list_.append(i_obj)
        return list_

    def get_reference_dict(self):
        query_dict = {}

        dict_ = collections.OrderedDict()
        p_end = r'fileInfo.*'

        p_0 = r'.*file.*'

        # load
        p_1 = r'.*file -rdi (.*?) -ns "(.*?)" -rfn.*?"(.*?)".*?-typ.*?"(.*?)".*?"(.*?)"'+self.SEP
        # unload
        p_2 = r'.*file -rdi (.*?) -ns "(.*?)" -dr 1 -rfn.*?"(.*?)".*?-typ.*?"(.*?)".*?"(.*?)"'+self.SEP
        for i_idx, i_line in enumerate(self._lines):
            # use match, search is slowly
            if re.match(p_end, i_line, re.DOTALL):
                break

            if re.match(p_0, i_line, re.DOTALL):
                i_r_1 = re.search(p_1, i_line, re.DOTALL)
                i_args = None
                if i_r_1:
                    i_namespace_local = i_r_1.group(2)
                    i_node = i_r_1.group(3)
                    i_file = i_r_1.group(5)
                    i_args = i_namespace_local, i_node, i_file, True
                else:
                    i_r_2 = re.search(p_2, i_line, re.DOTALL)
                    if i_r_2:
                        i_namespace_local = i_r_2.group(2)
                        i_node = i_r_2.group(3)
                        i_file = i_r_2.group(5)
                        i_args = i_namespace_local, i_node, i_file, False

                if i_args:
                    i_namespace_local, i_node, i_file, is_loaded = i_args
                    i_node_args = i_node.split(':')
                    i_namespace_parent = ':'.join(i_node_args[:-1])
                    i_node_name = i_node
                    if i_namespace_parent:
                        i_namespace = '{}:{}'.format(i_namespace_parent, i_namespace_local)

                        if i_namespace_parent in query_dict:
                            i_parent_path = query_dict[i_namespace_parent]
                            i_path = '{}/{}'.format(i_parent_path, i_node_name)
                        else:
                            i_path = '/{}'.format(i_node_name)
                    else:
                        i_namespace = i_namespace_local
                        i_path = '/{}'.format(i_node_name)

                    query_dict[i_namespace] = i_path

                    dict_[i_path] = dict(
                        namespace=i_namespace,
                        node=i_node,
                        type='reference',
                        file=i_file,
                        is_loaded=is_loaded,
                        icon_name='node/maya/reference'
                    )
        return dict_

    def get_references(self):
        list_ = []
        for k, v in self.get_reference_dict().items():
            i_obj = bsc_core.BscNodePathOpt(k)
            i_obj.set_properties(v)
            list_.append(i_obj)
        return list_

    def get_fps(self):
        p_0 = r'currentUnit.*'

        p_1 = r'currentUnit -l (.*?) -a (.*?) -t (.*?)'+self.SEP
        for i_idx, i_line in enumerate(self._lines):
            if re.match(p_0, i_line, re.DOTALL):
                i_r_1 = re.search(p_1, i_line, re.DOTALL)
                if i_r_1:
                    time_unit = i_r_1.group(3)
                    return _dcc_base.MayaTimeunit.timeunit_to_fps(time_unit)
        return 24

    def get_frame_range(self):
        p_0 = '.*playbackOptions.*'

        p_1 = r'.*?setAttr "\.b" -type "string" "playbackOptions -min (\d+) -max (\d+) -ast \d+ -aet \d+ "'+self.SEP
        for i_idx, i_line in enumerate(self._lines):
            if re.match(p_0, i_line, re.DOTALL):
                i_r_1 = re.search(p_1, i_line, re.DOTALL)
                if i_r_1:
                    start_frame, end_frame = i_r_1.group(1), i_r_1.group(2)
                    return int(start_frame), int(end_frame)
        return 1, 24

    def get_modify_time(self):
        line = self._lines[0]
        p_0 = '.*//Last modified: (.*?)\n.*'

        r_0 = re.search(p_0, line, re.DOTALL)

        time_0 = r_0.group(1)
        parsed_time = datetime.strptime(time_0, '%a, %b %d, %Y %I:%M:%S %p')
        time_b = parsed_time.strftime('%Y-%m-%d %H:%M:%S')
        return time_b
