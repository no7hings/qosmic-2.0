# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.dcc.core as bsc_dcc_core
# gui
import lxgui.core as gui_core

import lxgui.proxy.widgets as prx_widgets

import lxgui.proxy.scripts as gui_prx_scripts
# resolver
import lxresolver.core as rsv_core


class AbsDccComparerOpt(object):
    DCC_NAMESPACE = None
    DCC_NODE_CLS = None
    DCC_COMPONENT_CLS = None
    DCC_SELECTION_CLS = None
    DCC_PATHSEP = None

    def __init__(self, filter_tree_view, result_tree_view):
        self._prx_tree_view_for_filter = filter_tree_view
        self._result_tree_view = result_tree_view
        self._item_dict = self._result_tree_view._item_dict

        self._result_tree_view.connect_item_select_changed_to(
            self.set_select
        )

        self._filter_opt = gui_prx_scripts.GuiPrxScpForTreeTagFilter(
            prx_tree_view_src=self._prx_tree_view_for_filter,
            prx_tree_view_tgt=self._result_tree_view,
            prx_tree_item_cls=prx_widgets.PrxObjTreeItem
        )

    def restore_all(self):
        self._prx_tree_view_for_filter.restore_all()
        self._result_tree_view.restore_all()
        self._filter_opt.restore_all()

    def get_node(self, path_src, path_tgt, status, description):
        if path_src in self._item_dict:
            return self._item_dict[path_src]
        #
        dcc_path_dag_opt_src = bsc_core.PthNodeOpt(path_src)
        dcc_path_dag_opt_tgt = bsc_core.PthNodeOpt(path_tgt)
        #
        dcc_obj_src = self.DCC_NODE_CLS(path_src)

        transform_path_opt_src = dcc_path_dag_opt_src.get_parent()
        transform_prx_item_src = self.get_transform(transform_path_opt_src)
        #
        prx_item_src = transform_prx_item_src.add_child(
            name=[dcc_obj_src.name, description, dcc_path_dag_opt_tgt.name],
            icon=gui_core.GuiIcon.get('obj/mesh'),
            tool_tip=[path_src, description, path_tgt],
        )
        prx_item_src.set_status(
            status
        )
        self._item_dict[path_src] = prx_item_src
        prx_item_src.set_gui_dcc_obj(
            dcc_obj_src, self.DCC_NAMESPACE
        )

        self._filter_opt.register(
            prx_item_src, [description]
        )
        return prx_item_src

    def get_root(self, path_dag_opt):
        path = path_dag_opt.path
        if path in self._item_dict:
            return self._item_dict[path]

        prx_item = self._result_tree_view.create_item(
            name=path_dag_opt.name,
            icon=gui_core.GuiIcon.get('obj/transform'),
            tool_tip=path,
        )
        prx_item.set_expanded(True)
        self._item_dict[path] = prx_item
        return prx_item

    def get_group(self, path_dag_opt):
        path = path_dag_opt.path
        if path in self._item_dict:
            return self._item_dict[path]

        parent_prx_item = self.get_root(path_dag_opt.get_root())

        prx_item = parent_prx_item.add_child(
            name=path_dag_opt.name,
            icon=gui_core.GuiIcon.get('obj/transform'),
            tool_tip=path,
        )
        prx_item.set_expanded(True)
        self._item_dict[path] = prx_item
        return prx_item

    def get_transform(self, path_dag_opt):
        path = path_dag_opt.path
        if path in self._item_dict:
            return self._item_dict[path]

        name = path_dag_opt.name

        parent_prx_item = self.get_group(path_dag_opt.get_parent())

        prx_item = parent_prx_item.add_child(
            name=name,
            icon=gui_core.GuiIcon.get('obj/transform'),
            tool_tip=path,
        )
        prx_item.set_expanded(True)
        self._item_dict[path] = prx_item
        return prx_item

    def set_select(self):
        pass

    def set_accept(self):
        pass


class AbsPnlComparerForAssetGeometry(prx_widgets.PrxSessionWindow):
    ERROR_STATUS = [
        bsc_dcc_core.DccMeshCheckStatus.Deletion,
        bsc_dcc_core.DccMeshCheckStatus.Addition,
        #
        bsc_dcc_core.DccMeshCheckStatus.NameChanged,
        bsc_dcc_core.DccMeshCheckStatus.PathChanged,
        bsc_dcc_core.DccMeshCheckStatus.PathExchanged,
        #
        bsc_dcc_core.DccMeshCheckStatus.FaceVerticesChanged,
    ]
    WARNING_STATUS = [
        bsc_dcc_core.DccMeshCheckStatus.PointsChanged,
    ]
    DCC_COMPARER_OPT_CLS = None

    def set_all_setup(self):
        s = prx_widgets.PrxVScrollArea()
        self.add_widget(s)

        e_g = prx_widgets.PrxHToolGroup()
        s.add_widget(e_g)
        e_g.set_name('viewers')
        e_g.set_expanded(True)

        h_s = prx_widgets.PrxHSplitter()
        e_g.add_widget(h_s)
        v_s = prx_widgets.PrxVSplitter()
        h_s.add_widget(v_s)
        self._prx_tree_view_for_filter = prx_widgets.PrxTreeView()
        v_s.add_widget(self._prx_tree_view_for_filter)
        self._prx_tree_view_for_filter.set_header_view_create(
            [('name', 2), ('count', 1)],
            self.get_definition_window_size()[0]*(1.0/3.0)-48
        )
        #
        self._sector_chart = prx_widgets.PrxSectorChart()
        v_s.add_widget(self._sector_chart)
        self._result_tree_view = prx_widgets.PrxTreeView()
        h_s.add_widget(self._result_tree_view)
        self._result_tree_view.set_header_view_create(
            [('name', 2), ('description', 1), ('target', 1)],
            self.get_definition_window_size()[0]*(2.0/3.0)-48
        )
        #
        self._comparer_opt = self.DCC_COMPARER_OPT_CLS(
            self._prx_tree_view_for_filter, self._result_tree_view
        )
        #
        self._options_prx_node = prx_widgets.PrxNode('options')
        s.add_widget(self._options_prx_node)
        self._options_prx_node.create_ports_by_data(
            self._session.configure.get('build.node.options'),
        )

        self._options_prx_node.set(
            'refresh', self.set_refresh_all
        )

        self._set_collapse_update_(
            collapse_dict={
                'options': self._options_prx_node,
            }
        )

        v_s.set_stretches([1, 2])
        h_s.set_stretches([1, 2])

        self._resolver = rsv_core.RsvBase.generate_root()
        self._rsv_project = self._resolver.get_rsv_project(
            project=self._session.option_opt.get('project')
        )
        self._rsv_asset = self._rsv_project.get_rsv_resource(
            asset=self._session.option_opt.get('asset')
        )

        self.__set_usd_source_file_refresh_()
        self.__set_usd_target_file_refresh_()

        self.set_refresh_all()

    def __init__(self, session, *args, **kwargs):
        super(AbsPnlComparerForAssetGeometry, self).__init__(session, *args, **kwargs)

    def __set_usd_source_file_refresh_(self):
        step = self._session.option_opt.get('source_step')
        task = self._session.option_opt.get('source_task')

        keyword = 'asset-geometry-usd-payload-file'
        rsv_task = self._rsv_asset.get_rsv_task(
            step=step, task=task
        )
        if rsv_task is not None:
            file_rsv_unit = rsv_task.get_rsv_unit(
                keyword=keyword
            )
            file_paths = file_rsv_unit.get_result(
                version='all'
            )
            self._options_prx_node.set(
                'usd.source_file', file_paths
            )

    def __set_usd_target_file_refresh_(self):
        step = self._session.option_opt.get('step')
        task = self._session.option_opt.get('task')

        keyword = 'asset-geometry-usd-payload-file'
        rsv_task = self._rsv_asset.get_rsv_task(
            step=step, task=task
        )
        if rsv_task is not None:
            file_rsv_unit = rsv_task.get_rsv_unit(
                keyword=keyword
            )
            file_paths = file_rsv_unit.get_result(
                version='all'
            )
            self._options_prx_node.set(
                'usd.target_file', file_paths
            )

    def __gain_data_fnc_(self, file_path_src, file_path_tgt, location):
        import lxusd.fnc.objects as usd_fnc_objects

        self._comparer_results = usd_fnc_objects.FncComparerForGeometry(
            option=dict(
                file_src=file_path_src,
                file_tgt=file_path_tgt,
                #
                location=location
            )
        ).generate_results()

    def __build_data_fnc_(self):
        sector_chart_data_dict = {}
        count = len(self._comparer_results)

        self._comparer_opt.restore_all()

        with bsc_log.LogProcessContext.create(maximum=count, label='gui-add for geometry-comparer result') as g_p:
            for i_path_src, i_path_tgt, i_description in self._comparer_results:
                i_keys = i_description.split('+')

                for j_key in i_keys:
                    sector_chart_data_dict.setdefault(
                        j_key, []
                    ).append(
                        i_path_src
                    )

                i_status = gui_core.GuiDialog.ValidationStatus.Correct
                for j_key in i_keys:
                    if j_key in self.ERROR_STATUS:
                        i_status = gui_core.GuiDialog.ValidationStatus.Error
                        break
                    elif j_key in self.WARNING_STATUS:
                        i_status = gui_core.GuiDialog.ValidationStatus.Warning
                        break

                self._comparer_opt.get_node(
                    i_path_src, i_path_tgt, i_status, i_description
                )
                #
                g_p.do_update()
        #
        sector_chart_data = []
        for i_check_status in bsc_dcc_core.DccMeshCheckStatus.All:
            if i_check_status != bsc_dcc_core.DccMeshCheckStatus.NonChanged:
                if i_check_status in sector_chart_data_dict:
                    sector_chart_data.append(
                        (i_check_status, count, len(sector_chart_data_dict[i_check_status]))
                    )
                else:
                    sector_chart_data.append(
                        (i_check_status, count, 0)
                    )
        #
        self._sector_chart.set_chart_data(
            sector_chart_data,
            gui_core.GuiSectorChartMode.Error
        )

        self._comparer_opt.set_accept()

    def set_refresh_all(self):
        file_path_src = self._options_prx_node.get('usd.source_file')
        if not file_path_src:
            return
        file_path_tgt = self._options_prx_node.get('usd.target_file')
        if not file_path_tgt:
            return

        location = '/master/hi'

        self._comparer_results = []

        ms = [
            # gain data
            (self.__gain_data_fnc_, (file_path_src, file_path_tgt, location)),
            # comparer
            (self.__build_data_fnc_, ())
        ]
        with bsc_log.LogProcessContext.create(maximum=len(ms), label='execute gui-build method') as g_p:
            for i_method, i_args in ms:
                g_p.do_update()
                i_method(*i_args)
