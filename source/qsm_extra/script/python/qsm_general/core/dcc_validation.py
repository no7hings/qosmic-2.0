# coding:utf-8
import six

import lxbasic.core as bsc_core

import lxbasic.resource as bsc_resource

import lxgui.core as gui_core


class DccValidationOptions(object):
    def __init__(self, key):
        self._language = bsc_core.EnvBaseMtd.get_ui_language()
        self._options_cfg = bsc_resource.RscExtendConfigure.get_as_content(key)
        self._options_cfg.do_flatten()

    @property
    def configure(self):
        return self._options_cfg

    def to_convertion_name(self, key):
        _ = self._options_cfg.get('convertion.{}'.format(key))
        if not _:
            print key
            raise RuntimeError()
        return gui_core.GuiUtil.choice_name(
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

    def to_text(self, data):
        file_path = data['file']
        result_data = data['results']
        indent = 2
        start_index = 0

        if result_data:
            texts = [
                file_path
            ]
            process_options = self.generate_process_options()
            for i_branch, i_leafs in process_options.items():
                texts.append(
                    six.u('{}{}').format(
                        (start_index+0)*indent*' ',
                        self.to_convertion_name(i_branch)
                    )
                )
                if i_branch in result_data:
                    i_branch_data = result_data[i_branch]
                    for j_leaf in i_leafs:
                        texts.append(
                            six.u('{}{}').format(
                                (start_index+1)*indent*' ',
                                self.to_convertion_name(j_leaf)
                            )
                        )
                        j_leaf_options = self.get_leaf_options_at(i_branch, j_leaf)
                        # has result
                        if j_leaf in i_branch_data:
                            texts.append(
                                six.u('{}{}').format(
                                    (start_index+2)*indent*' ',
                                    self.to_convertion_name(j_leaf_options['level'])
                                )
                            )
                            j_leaf_data = i_branch_data[j_leaf]
                            if j_leaf_data:
                                j_description = gui_core.GuiUtil.choice_description(
                                    self._language, j_leaf_options
                                )
                                for k in j_leaf_data:
                                    k_name, k_description_kwargs_list = k
                                    texts.append(
                                        six.u('{}{}').format(
                                            (start_index+3)*indent*' ',
                                            k_name
                                        )
                                    )
                                    for l_description_kwargs in k_description_kwargs_list:
                                        texts.append(
                                            six.u('{}{}').format(
                                                (start_index+4)*indent*' ',
                                                j_description.format(**l_description_kwargs)
                                            )
                                        )
                        else:
                            texts.append(
                                six.u('{}{}').format(
                                    (start_index+2)*indent*' ',
                                    self.to_convertion_name('pass')
                                )
                            )
                else:
                    texts.append(
                        six.u('{}{}').format(
                            (start_index+1)*indent*' ',
                            self.to_convertion_name('pass')
                        )
                    )
        else:
            texts = [
                six.u('{}\n{}').format(
                    file_path,
                    self.to_convertion_name('pass')
                )
            ]
        return six.u('\n').join(texts)


if __name__ == '__main__':
    print DccValidationOptions('rig/adv_validation_options').generate_process_options()
