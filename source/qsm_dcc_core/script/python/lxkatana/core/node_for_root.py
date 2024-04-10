# coding:utf-8
import collections

import lxcontent.core as ctt_core

import lxresource as bsc_resource

import lxgui.core as gui_core
# katana
from .wrap import *

from . import base as ktn_cor_base

from . import node as ktn_cor_node


class VariablesSetting(object):
    def __init__(self):
        self._ktn_obj = NodegraphAPI.GetNode('rootNode')

    def set(self, key, value):
        port_path = 'variables.{}.options'.format(key)
        p = self._ktn_obj.getParameter(port_path)
        if p is None:
            pass
        ktn_cor_node.NGPortOpt(p).set(value)

    def get(self, key):
        pass

    def get_branches(self, key):
        p = self._ktn_obj.getParameter('variables.{}.options'.format(key))
        if p:
            return ktn_cor_node.NGPortOpt(p).get()
        return []

    def register(self, key, values):
        ktn_port = self._ktn_obj.getParameter('variables')
        group_ktn_port = ktn_port.getChild(key)
        if group_ktn_port is not None:
            ktn_port.deleteChild(group_ktn_port)
            _ = ktn_cor_node.NGNodeOpt(self._ktn_obj).get_port_raw('variables.{}.value'.format(key))
            if _ in values:
                value = _
            else:
                value = values[0]
        else:
            value = values[0]
        #
        group_ktn_port = ktn_port.createChildGroup(key)
        group_ktn_port.createChildNumber('enable', 1)
        group_ktn_port.createChildString('value', value)
        c = len(values)
        #
        options_port = group_ktn_port.createChildStringArray('options', c)
        for i in range(c):
            i_ktn_port = options_port.getChildByIndex(i)
            i_ktn_port.setValue(values[i], 0)

    def set_register_by_configure(self, dic):
        for k, v in dic.items():
            self.register(k, v)

    def get_variants(self):
        dic = collections.OrderedDict()
        ktn_port = self._ktn_obj.getParameter('variables')
        for i in ktn_port.getChildren():
            i_key = ktn_cor_node.NGPortOpt(i).name
            i_values = ktn_cor_node.NGPortOpt(
                self._ktn_obj.getParameter('variables.{}.options'.format(i_key))
            ).get()
            dic[i_key] = i_values
        return dic


class WorkspaceSetting(object):
    def __init__(self):
        self._cfg = ctt_core.Content(
            value=bsc_resource.RscExtendConfigure.get_yaml(
                'katana/script/scene'
            )
        )
        self._cfg.do_flatten()
        self._obj_opt = ktn_cor_node.NGNodeOpt(NodegraphAPI.GetNode('rootNode'))

    def setup(self):
        # self._obj_opt.clear_ports(self._cfg.get('main.clear_start'))
        self._obj_opt.create_ports_by_data(
            self._cfg.get('main.ports')
        )

    def build_env_ports(self):
        root = self._cfg.get('main.environment.root')
        if self._obj_opt.get_port_is_exists(root) is False:
            # self._obj_opt.clear_ports(root)
            self._obj_opt.create_ports_by_data(
                self._cfg.get('main.environment.ports')
            )

    def save_env(self, index, key, env_key, env_value):
        root = self._cfg.get('main.environment.root')
        self._obj_opt.set(
            '{}.data_{}.i0'.format(root, index), key, ignore_changed=True
        )
        self._obj_opt.set(
            '{}.data_{}.i1'.format(root, index), env_key, ignore_changed=True
        )
        self._obj_opt.set(
            '{}.data_{}.i2'.format(root, index), env_value, ignore_changed=True
        )

    def get_env_data(self):
        data = []
        root = self._cfg.get('main.environment.root')
        for i_index in range(20):
            i_key = self._obj_opt.get(
                '{}.data_{}.i0'.format(root, i_index)
            )
            i_env_key = self._obj_opt.get(
                '{}.data_{}.i1'.format(root, i_index)
            )
            i_env_value = self._obj_opt.get(
                '{}.data_{}.i2'.format(root, i_index)
            )
            if i_key and i_env_key and i_env_value:
                data.append(
                    (i_key, i_env_key, i_env_value)
                )
        return data

    def get_task_kwargs(self):
        dict_ = {}
        data = self.get_env_data()
        for i_index, (i_key, i_env_key, i_env_value) in enumerate(data):
            dict_[i_key] = i_env_value
        return dict_

    def build_look_ports(self):
        root = self._cfg.get('main.look.root')
        if self._obj_opt.get_port_is_exists(root) is False:
            # self._obj_opt.clear_ports(root)
            self._obj_opt.create_ports_by_data(
                self._cfg.get('main.look.ports')
            )

    @classmethod
    def get_look_output_nodes(cls):
        return ktn_cor_node.NGNodesMtd.find_nodes(
            type_name='LookFileBake', ignore_bypassed=True
        )

    @classmethod
    def get_look_output_node_opts(cls):
        return [
            ktn_cor_node.NGNodeOpt(i) for i in cls.get_look_output_nodes()
        ]

    def set_current_look_output(self, node_name):
        root = self._cfg.get('main.look.root')
        self._obj_opt.set(
            '{}.output'.format(root), node_name
        )

    def get_current_look_output(self):
        root = self._cfg.get('main.look.root')
        return self._obj_opt.get(
            '{}.output'.format(root)
        )

    def get_current_look_output_opt(self):
        _ = self.get_current_look_output()
        if _:
            if ktn_cor_node.NGNodeOpt._get_is_exists_(_):
                return ktn_cor_node.NGNodeOpt(_)

    def update_current_look_output_with_dialog(self):
        if ktn_cor_base.KtnUtil.get_is_ui_mode():
            opts = self.get_look_output_node_opts()
            if opts:
                if len(opts) > 1:
                    def yes_fnc_():
                        _n = o.get('dcc.node')
                        self.set_current_look_output(_n)

                    #
                    w = gui_core.GuiDialog.create(
                        'Workspace Setting',
                        content=(
                            'More then one "LookFileBake" in scene:\n'
                            '   1, choose one use as current\n'
                            '   2, press "Confirm" to continue'
                        ),
                        status=gui_core.GuiDialog.ValidationStatus.Warning,
                        options_configure=self._cfg.get('main.look.dialog_options'),
                        #
                        yes_method=yes_fnc_,
                        #
                        yes_label='Confirm',
                        #
                        no_visible=False, cancel_visible=False,
                        show=False,
                        window_size=(480, 240)
                    )

                    o = w.get_options_node()

                    o.set('dcc.node', [i.get_name() for i in opts])

                    w.set_window_show()

                    if w.get_result() is True:
                        return self.get_current_look_output()
                else:
                    name = opts[0].get_name()
                    self.set_current_look_output(name)
                    return name

    def get_current_look_output_opt_force(self):
        opt = self.get_current_look_output_opt()
        if opt is not None:
            return opt
        else:
            opts = self.get_look_output_node_opts()
            if opts:
                if len(opts) > 1:
                    if ktn_cor_base.KtnUtil.get_is_ui_mode():
                        def yes_fnc_():
                            _n = o.get('dcc.node')
                            self.set_current_look_output(_n)

                        #
                        w = gui_core.GuiDialog.create(
                            'Workspace Setting',
                            content=(
                                'More then one "LookFileBake" in scene:\n'
                                '   1, choose one use as current\n'
                                '   2, press "Confirm" to continue'
                            ),
                            status=gui_core.GuiDialog.ValidationStatus.Warning,
                            options_configure=self._cfg.get('main.look.dialog_options'),
                            #
                            yes_method=yes_fnc_,
                            #
                            yes_label='Confirm',
                            #
                            no_visible=False, cancel_visible=False,
                            show=False,
                            window_size=(480, 240)
                        )

                        o = w.get_options_node()

                        o.set('dcc.node', [i.get_name() for i in opts])

                        w.set_window_show()

                        if w.get_result() is True:
                            return self.get_current_look_output_opt()
                    else:
                        return opts[0]
                else:
                    return opts[0]
