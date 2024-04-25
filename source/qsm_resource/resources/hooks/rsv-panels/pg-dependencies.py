# coding:utf-8
import lxbasic.core as bsc_core

import lxgui.core as gui_core

import lxgui.proxy.widgets as prx_widgets

import lxgui.proxy.core as gui_prx_core

import lxgui.proxy.scripts as gui_prx_scripts


class PGDependencies(prx_widgets.PrxSessionWindow):
    NAMESPACE = 'storage'

    def __init__(self, session, *args, **kwargs):
        super(PGDependencies, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):
        self._gui_data = []
        self._target_format_create_data = []
        self._target_color_space_create_data = []
        #
        self._viewer_group = prx_widgets.PrxHToolGroup()
        self.add_widget(self._viewer_group)
        self._viewer_group.set_name('dependencies')
        self._viewer_group.set_expanded(True)
        #
        h_s = prx_widgets.PrxHSplitter()
        self._viewer_group.add_widget(h_s)
        self._prx_tree_view_for_filter = prx_widgets.PrxTreeView()
        h_s.add_widget(self._prx_tree_view_for_filter)
        self._prx_tree_view_for_filter.create_header_view(
            [('name', 3), ('count', 1)],
            self.get_definition_window_size()[0]*(1.0/4.0)-32
        )
        #
        self._result_tree_view = prx_widgets.PrxTreeView()
        h_s.add_widget(self._result_tree_view)
        h_s.set_stretches([1, 3])
        #
        self._filter_tree_view_opt = gui_prx_scripts.GuiPrxScpForTreeTagFilter(
            prx_tree_view_src=self._prx_tree_view_for_filter,
            prx_tree_view_tgt=self._result_tree_view,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )
        #
        self._options_prx_node = prx_widgets.PrxNode('options')
        self.add_widget(self._options_prx_node)
        self._options_prx_node.create_ports_by_data(
            self._session.configure.get('build.node.options'),
        )
        #
        self._set_collapse_update_(
            collapse_dict={
                'options': self._options_prx_node,
            }
        )

        self._options_prx_node.set(
            'refresh', self.set_refresh_all
        )

        self.set_refresh_all()

    def _get_file_(self):
        return self._options_prx_node.get(
            'file'
        )

    def _get_data_(self):
        list_ = []
        for i in range(100):
            list_.append(
                (('file', '/temp/test_{}.exr'.format(i)), ('project', 'cgm'), ('asset', 'test_{}'.format(i)),
                 ('step', 'mod'), ('task', 'modeling'))
            )
        return list_

    def _set_item_show_deferred_(self, prx_item, names):
        prx_item.set_names(names)

    def _add_item_(self, key, names, filter_tags):
        create_kwargs = dict(
            name='loading ...',
            icon=gui_core.GuiIcon.get('file/file'),
            filter_key=key
        )
        prx_item = self._result_tree_view.create_item(**create_kwargs)
        self._filter_tree_view_opt.register(
            prx_item, filter_tags
        )
        prx_item.set_show_build_fnc(
            lambda *args, **kwargs: self._set_item_show_deferred_(prx_item, names)
        )

    def set_refresh_all(self):
        self._filter_keys = [
            'project',
            'asset',
            'step',
            'task'
        ]

        self._result_tree_view.create_header_view(
            [(i, 2) for i in self._filter_keys],
            self.get_definition_window_size()[0]*(3.0/4.0)-32
        )
        self._filter_tree_view_opt.restore_all()
        self._result_tree_view.set_clear()
        for i in self._get_data_():
            key = '&'.join(['{}={}'.format(*j) for j in i])
            names = [j[1] for j in i]
            filter_tags = ['.'.join([bsc_core.SPathMtd.set_quote_to(k) for k in j]) for j in i]
            self._add_item_(key, names, filter_tags)

        # self._filter_tree_view_opt.set_filter_statistic()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
        PGDependencies, session=session
    )
