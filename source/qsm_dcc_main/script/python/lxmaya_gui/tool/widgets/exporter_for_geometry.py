# coding:utf-8
import lxbasic.dcc.objects as bsc_dcc_objects

import lxgui.proxy.widgets as prx_widgets


class PnlExporterForAssetGeometry(prx_widgets.PrxSessionToolWindow):
    def __init__(self, session, *args, **kwargs):
        super(PnlExporterForAssetGeometry, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):
        self._options_prx_node = prx_widgets.PrxNode('options')
        self.add_widget(self._options_prx_node)
        self._options_prx_node.create_ports_by_data(
            self._session.configure.get('build.node.options'),
        )

        self.post_setup_fnc()
        self.refresh_components()

    def post_setup_fnc(self):
        import lxresolver.core as rsv_core

        import lxresolver.scripts as rsv_scripts

        import lxgui.core as gui_core

        session = self.session

        env_data = rsv_scripts.ScpEnvironment.get_as_dict()

        self._resolver = rsv_core.RsvBase.generate_root()

        self._rsv_task = self._resolver.get_rsv_task(
            **env_data
        )
        if self._rsv_task is not None:
            self._rsv_project = self._rsv_task.get_rsv_project()

            self._dcc_data = self._rsv_project.get_dcc_data(application='maya')

            keyword = 'asset-source-geometry-usd-payload-file'

            rsv_unit = self._rsv_task.get_rsv_unit(
                keyword=keyword
            )

            result = rsv_unit.get_result('new')

            o = self._options_prx_node

            o.set('usd.file', result)

            o.get_port('renderable.components').connect_input_changed_to(
                self.refresh_components
            )
            o.set('renderable.export', self.export_renderable_fnc_)
            o.get_port('auxiliary.components').connect_input_changed_to(
                self.refresh_components
            )
            o.set('auxiliary.export', self.export_auxiliary_fnc_)
        else:
            gui_core.GuiDialog.create(
                session.gui_name,
                content='open a task scene file and retry',
                status=gui_core.GuiDialog.ValidationStatus.Error,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False,
                #
                parent=self.widget
            )
            #
            self.close_window_later()

    def export_renderable_fnc_(self):
        file_path = self._options_prx_node.get('usd.file')
        p = self._options_prx_node.get_port('geometry.components')
        renderable_locations = [i.get_path() for i in p.get_all() if i.get_type_name() == 'renderable']
        if file_path and renderable_locations:
            import lxmaya.fnc.objects as mya_fnc_objects

            mya_fnc_objects.FncExporterForGeometryUsdNew(
                option=dict(
                    file=file_path,
                    renderable_locations=renderable_locations,
                )
            ).execute()

    def export_auxiliary_fnc_(self):
        file_path = self._options_prx_node.get('usd.file')
        p = self._options_prx_node.get_port('geometry.components')
        auxiliary_locations = [i.get_path() for i in p.get_all() if i.get_type_name() == 'auxiliary']
        if file_path and auxiliary_locations:
            import lxmaya.fnc.objects as mya_fnc_objects

            mya_fnc_objects.FncExporterForGeometryUsdNew(
                option=dict(
                    file=file_path,
                    auxiliary_locations=auxiliary_locations,
                )
            ).execute()

    def apply_fnc(self):
        file_path = self._options_prx_node.get('usd.file')
        p = self._options_prx_node.get_port('geometry.components')
        renderable_locations = [i.get_path() for i in p.get_all() if i.get_type_name() == 'renderable']
        auxiliary_locations = [i.get_path() for i in p.get_all() if i.get_type_name() == 'auxiliary']
        if file_path and (renderable_locations or auxiliary_locations):
            import lxmaya.fnc.objects as mya_fnc_objects

            mya_fnc_objects.FncExporterForGeometryUsdNew(
                option=dict(
                    file=file_path,
                    renderable_locations=renderable_locations,
                    auxiliary_locations=auxiliary_locations,
                )
            ).execute()

    def refresh_components(self):
        objs = []
        for i_branch_key in ['renderable', 'auxiliary']:
            i_leafs = self._options_prx_node.get('{}.components'.format(i_branch_key)) or []
            for j_leaf in i_leafs:
                j_leaf_location = self._dcc_data.get(
                    '{}.{}'.format(i_branch_key, j_leaf)
                )
                if i_branch_key == 'renderable':
                    j_obj = bsc_dcc_objects.Node(j_leaf_location, type_name=i_branch_key, icon_name='obj/renderable')
                elif i_branch_key == 'auxiliary':
                    j_obj = bsc_dcc_objects.Node(j_leaf_location, type_name=i_branch_key, icon_name='obj/non-renderable')
                else:
                    raise RuntimeError()
                #
                objs.append(j_obj)
        #
        self._options_prx_node.set(
            'geometry.components', objs
        )
