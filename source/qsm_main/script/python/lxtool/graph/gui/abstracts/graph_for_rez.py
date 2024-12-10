# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxuniverse.objects as unr_objects

import lxgui.proxy.widgets as gui_prx_widgets

import lxgui.qt.core as gui_qt_core


class AbsRezGraph(gui_prx_widgets.PrxBaseWindow):
    OPTION_HOOK_KEY = None

    def __init__(self, hook_option, *args, **kwargs):
        super(AbsRezGraph, self).__init__(*args, **kwargs)
        if hook_option is not None:
            self._hook_option_opt = bsc_core.ArgDictStringOpt(hook_option)
            self._hook_option_opt.set(
                'option_hook_key', self.OPTION_HOOK_KEY
            )

            import lxsession.commands as ssn_commands
            #
            self._option_hook_configure = ssn_commands.get_option_hook_configure(
                self._hook_option_opt.to_string()
            )
            #
            self._hook_gui_configure = self._option_hook_configure.get_as_content('option.gui')
            #
            raw = bsc_core.BscEnviron.get('QSM_TEST')
            if raw:
                self._test_flag = True
            else:
                self._test_flag = False

            if self._test_flag:
                self.set_window_title(
                    '[BETA] {}'.format(self._hook_gui_configure.get('name'))
                )
            else:
                self.set_window_title(
                    self._hook_gui_configure.get('name')
                )
            #
            self.set_window_icon_name_text(
                self._hook_gui_configure.get('name')
            )
            self.set_definition_window_size(
                self._hook_gui_configure.get('size')
            )

            self.start_window_loading(
                self._set_tool_panel_setup_
            )

    def _set_tool_panel_setup_(self):
        h_s = gui_prx_widgets.PrxHSplitter()
        self.add_widget(h_s)
        self._node_tree = gui_prx_widgets.PrxNGTree()
        h_s.add_widget(self._node_tree)
        self._node_graph = gui_prx_widgets.PrxNGGraph()
        h_s.add_widget(self._node_graph)

        h_s.set_stretches([1, 3])

        packages = self._hook_option_opt.get('packages', as_array=True)
        self.test(packages)

    def test(self, packages):
        import rez.resolved_context as r_c

        u = unr_objects.ObjUniverse()

        r_s_t = u.create_obj_type('rez', 'system')
        r_p_t = u.create_obj_type('rez', 'package')
        r_v_t = u.create_obj_type('rez', 'v')

        t = u.create_type(u.Category.CONSTANT, u.Type.NODE)

        r = r_c.ResolvedContext(
            packages,
        )

        root = u.get_root()
        root.create_input(
            t, 'input'
        )
        root.create_output(
            t, 'output'
        )

        path_dict = {}
        for i_key in packages:
            if '-' in i_key:
                i_type = r_v_t
                i_package, i_version = i_key.split('-')
                i_path = '/{}-{}'.format(i_package, i_version)
                i_n = i_type.create_obj(
                    i_path
                )
                i_n.create_input(
                    t, 'input'
                )
                i_n.create_output(
                    t, 'output'
                )
                root.get_input_port(
                    'input'
                ).set_source(
                    i_n.get_output_port(
                        'output'
                    )
                )
            else:
                i_package = i_key
                i_type = r_p_t
                i_path = '/{}'.format(i_package)

                i_p_n = i_type.create_obj(
                    i_path
                )
                i_p_n.create_input(
                    t, 'input'
                )
                i_p_n.create_output(
                    t, 'output'
                )
                root.get_input_port(
                    'input'
                ).set_source(
                    i_p_n.get_output_port(
                        'output'
                    )
                )

        g = r.graph()

        for i in g.nodes():
            i_atr = g.node_attributes(i)
            i_key = i_atr[0][1]
            if i_key.startswith('~'):
                i_type = r_s_t
                i_path = '/{}'.format(i_key)
            else:
                if '-' in i_key:
                    i_type = r_v_t
                    i_name, i_version = i_key.split('-')
                    if '[' in i_version:
                        if '[]' in i_version:
                            i_version_ = i_version[:-2]
                            i_path = '/{}-{}'.format(i_name, i_version_)
                        else:
                            i_version_ = i_version.split('[')[0]
                            i_index = i_version.split('[')[-1][:-1]
                            i_path = '/{}-{}-({})'.format(i_name, i_version_, i_index)
                    else:
                        i_path = '/{}-{}'.format(i_name, i_version)
                else:
                    i_type = r_p_t
                    i_path = '/{}'.format(i_key)
            #
            i_n = i_type.create_obj(
                i_path
            )
            i_n.create_input(
                t, 'input'
            )
            i_n.create_output(
                t, 'output'
            )
            path_dict[i] = i_path

        for i in g.edges():
            i_tgt, i_src = i
            i_src_path, i_tgt_path = path_dict[i_src], path_dict[i_tgt]
            i_n_src = u.get_obj(i_src_path)
            i_n_tgt = u.get_obj(i_tgt_path)
            i_n_src.get_output_port('output').connect_to(
                i_n_tgt.get_input_port('input')
            )

        self._node_graph.set_graph_universe(u)
        self._node_graph.set_node_show()

        self._node_tree.set_graph_universe(u)

        menu = self.create_menu(
            'Tool(s)'
        )
        menu.set_menu_data(
            [
                ('Save Graph', None, self._set_graph_save_),
            ]
        )

    def _set_graph_save_(self):
        size = self._node_graph.widget.size()
        p = gui_qt_core.QtGui.QPixmap(size)
        p.fill(gui_qt_core.QtCore.Qt.transparent)
        self._node_graph.widget.render(
            p
        )
        p.save('/data/f/rez_test/png/test_0.png', 'PNG')