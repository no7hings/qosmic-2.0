# coding:utf-8
import six

import lxbasic.core as bsc_core

import lxbasic.html as bsc_html

import lxbasic.resource as bsc_resource

import lxgui.core as gui_core

import qsm_general.core as qsm_gnl_core


class DccValidationOptions(object):

    def __init__(self, key):
        self._key = key
        self._language = bsc_core.BscEnviron.get_gui_language()
        self._options_cfg = bsc_resource.BscConfigure.get_as_content(key)
        self._options_cfg.do_flatten()

    @property
    def configure(self):
        return self._options_cfg

    def get_branches(self):
        return self._options_cfg.get('options')

    def get_leafs_at(self, branch):
        _ = self._options_cfg.get('options.{}'.format(branch))
        if _:
            return list(_.keys())
        return []

    def to_convertion_name(self, key):
        _ = self._options_cfg.get('convertion.{}'.format(key))
        if not _:
            raise RuntimeError(key)
        return gui_core.GuiUtil.choice_gui_name(
            self._language, _
        )

    def get_leaf_is_enable_at(self, branch, leaf):
        return self._options_cfg.get('options.{}.{}.enable'.format(branch, leaf))

    def get_leaf_options_at(self, branch, leaf):
        return self._options_cfg.get('options.{}.{}'.format(branch, leaf))

    def generate_process_options(self):
        dict_ = {}
        options = self._options_cfg.get('options')
        for i_branch, i_v in options.items():
            for j_leaf, j_options in i_v.items():
                if j_options['enable'] is True:
                    dict_.setdefault(i_branch, []).append(j_leaf)

            if i_branch in dict_:
                i_leafs = dict_[i_branch]
                if i_leafs:
                    i_leafs.sort()

        return dict_

    def update_process_options(self, process_options):
        options = self._options_cfg.get('options')
        for i_branch, i_v in options.items():
            i_branch_data = process_options.get(i_branch, {})
            for j_leaf, j_options in i_v.items():
                if j_leaf in i_branch_data:
                    j_options['enable'] = True
                else:
                    j_options['enable'] = False

    def update_process_options_to(self, process_options):
        opt = self.__class__(self._key)
        opt.update_process_options(process_options)
        return opt

    def to_result_args(self, data, mesh_count_result_data=None, component_mesh_count_result_data=None):
        result = 'pass'
        result_dict = {}

        file_path = data['file']
        result_data = data['results']
        if mesh_count_result_data:
            result_data.update(mesh_count_result_data)
        if component_mesh_count_result_data:
            result_data.update(component_mesh_count_result_data)

        formatter = bsc_html.HtmlFormatter()

        if result_data:
            formatter.new_line(
                file_path,
                indent=0
            )
            process_options = self.generate_process_options()
            for i_branch, i_leafs in process_options.items():
                if i_branch in result_data:
                    formatter.new_line(
                        self.to_convertion_name(i_branch), indent=1
                    )
                    i_branch_data = result_data[i_branch]
                    for j_leaf in i_leafs:
                        j_leaf_options = self.get_leaf_options_at(i_branch, j_leaf)
                        # has result
                        if j_leaf in i_branch_data:
                            formatter.new_line(
                                u'{} '.format(self.to_convertion_name(j_leaf)), indent=2
                            )
                            j_level = j_leaf_options['level']
                            j_value_limit = j_leaf_options.get('limit_value')

                            if j_level == 'error':
                                j_color = 'red'
                                result = 'error'
                                result_dict.setdefault(
                                    'error', []
                                ).append(j_leaf)
                            elif j_level == 'warning':
                                j_color = 'yellow'
                                # ignore result is error
                                if result == 'pass':
                                    result = 'warning'
                                result_dict.setdefault(
                                    'warning', []
                                ).append(j_leaf)
                            else:
                                j_color = 'default'

                            formatter.append_line(
                                self.to_convertion_name(j_level),
                                color=j_color
                            )

                            j_leaf_data = i_branch_data[j_leaf]
                            if j_leaf_data:
                                j_description = gui_core.GuiUtil.choice_gui_description(
                                    self._language, j_leaf_options
                                )
                                for k in j_leaf_data:
                                    k_name, k_description_kwargs_list = k
                                    if k_name is not None:
                                        formatter.new_line(
                                            k_name,
                                            indent=3
                                        )
                                        k_add = 1
                                    else:
                                        k_add = 0

                                    for l_description_kwargs in k_description_kwargs_list:
                                        if j_value_limit:
                                            l_description_kwargs['limit_value'] = j_value_limit

                                        l_kwargs = dict()
                                        for m_k, m_v in l_description_kwargs.items():
                                            if isinstance(m_v, int):
                                                m_v = bsc_core.BscInteger.to_prettify(m_v, language=self._language)
                                            l_kwargs[m_k] = bsc_core.ensure_unicode(m_v)

                                        formatter.new_line(
                                            j_description.format(**l_kwargs),
                                            indent=3+k_add, color=j_color
                                        )
                        else:
                            formatter.new_line(
                                u'{} '.format(self.to_convertion_name(j_leaf)), indent=2
                            )
                            formatter.append_line(
                                self.to_convertion_name('pass'),
                                color='green'
                            )
                else:
                    formatter.new_line(
                        u'{} '.format(self.to_convertion_name(i_branch)), indent=1
                    )
                    formatter.append_line(
                        self.to_convertion_name('pass'),
                        color='green',
                    )
        else:
            formatter.new_line(
                u'{} '.format(file_path),
                indent=0
            )
            formatter.append_line(
                self.to_convertion_name('pass'),
                color='green'
            )

        result_description = self.to_convertion_name('pass')
        if result_dict:
            strings = []
            for k, v in result_dict.items():
                i_string = u'{}x{}'.format(self.to_convertion_name(k), len(v))
                strings.append(i_string)

            result_description = u', '.join(strings)

        return result, result_description, formatter.to_html()

    def to_result_dict_for_mesh_count(self, data):
        branch = 'mesh_count'
        if data:
            result_dict = {}
            mesh_count_data_opt = qsm_gnl_core.MeshCountDataOpt(data['mesh_count'])
            process_options = self.generate_process_options()
            if branch in process_options:
                branch_dict = {}
                branch_options = process_options['mesh_count']
                for i_leaf in branch_options:
                    i_leaf_options = self.get_leaf_options_at(branch, i_leaf)
                    i_value = mesh_count_data_opt.__getattribute__(i_leaf)

                    i_limit_value = i_leaf_options['limit_value']
                    if i_value > i_limit_value:
                        if isinstance(i_value, float):
                            i_value = round(i_value, 3)
                        branch_dict[i_leaf] = [[None, [dict(value=i_value)]]]

                if branch_dict:
                    result_dict[branch] = branch_dict

            if result_dict:
                return result_dict
        return {}

    def to_result_dict_for_component_mesh_count(self, data):
        branch = 'component_mesh_count'
        if data:
            result_dict = {}
            mesh_count_data_opt = qsm_gnl_core.MeshCountDataOpt(data['mesh_count'])
            process_options = self.generate_process_options()
            if branch in process_options:
                branch_dict = {}
                branch_options = process_options['component_mesh_count']
                for i_leaf in branch_options:
                    i_leaf_options = self.get_leaf_options_at(branch, i_leaf)
                    i_limit_value = i_leaf_options['limit_value']
                    if i_leaf == 'component_triangle':
                        i_components = mesh_count_data_opt.components
                        if i_components:
                            i_result_list = []
                            for j_path, j_data in i_components.items():
                                j_value = j_data['triangle']
                                if j_value > i_limit_value:
                                    i_result_list.append(
                                        [j_path, [dict(value=j_value)]]
                                    )

                            if i_result_list:
                                branch_dict[i_leaf] = i_result_list
                    elif i_leaf == 'cache_triangle':
                        i_gpu_caches = mesh_count_data_opt.gpu_caches
                        if i_gpu_caches:
                            i_result_list = []
                            for j_path, j_data in i_gpu_caches.items():
                                j_value = j_data['triangle']
                                if j_value > i_limit_value:
                                    i_result_list.append(
                                        [j_path, [dict(value=j_value)]]
                                    )

                            if i_result_list:
                                branch_dict[i_leaf] = i_result_list

                if branch_dict:
                    result_dict[branch] = branch_dict

            if result_dict:
                return result_dict
        return {}
