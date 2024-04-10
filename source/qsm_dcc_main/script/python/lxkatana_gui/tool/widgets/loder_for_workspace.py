# coding:utf-8
import lxgui.proxy.widgets as prx_widgets

import lxkatana.core as ktn_core


class PnlLoaderForWorkspaceDcc(prx_widgets.PrxSessionToolWindow):
    def __init__(self, session, *args, **kwargs):
        super(PnlLoaderForWorkspaceDcc, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):
        self._options_prx_node = prx_widgets.PrxNode('options')
        self.add_widget(self._options_prx_node)
        self._options_prx_node.create_ports_by_data(
            self._session.configure.get('build.node.options'),
        )
        self.post_setup_fnc()

    def post_setup_fnc(self):
        import lxresolver.core as rsv_core

        import lxresolver.scripts as rsv_scripts

        import lxgui.core as gui_core

        session = self.session

        env_data = rsv_scripts.ScpEnvironment.get_as_dict()

        self._resolver = rsv_core.RsvBase.generate_root()

        self._rsv_project = self._resolver.get_rsv_project(
            **env_data
        )
        if self._rsv_project is not None:
            self._rsv_task = self._rsv_project.get_rsv_task(
                step=self._rsv_project.properties.get('project_steps.surface'),
                task=self._rsv_project.properties.get('project_tasks.template')
            )
            if self._rsv_task:
                o = self._options_prx_node
                o.get_port('area').connect_input_changed_to(
                    self.refresh_auto_fnc
                )
                o.get_port('team.file').connect_refresh_action_for(
                    self.refresh_team_file_fnc
                )
                o.get_port('artist.name').connect_input_changed_to(
                    self.refresh_artist_file_fnc
                )
                o.get_port('artist.file').connect_refresh_action_for(
                    self.refresh_artist_file_fnc
                )
                self.refresh_auto_fnc()
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

    def refresh_artist_file_fnc(self):
        o = self._options_prx_node
        artist = o.get('artist.name')
        if artist != 'None':
            p = o.get_port('artist.file')

            keyword_0 = 'project-user-katana-scene-src-dir'
            keyword_1 = 'project-user-katana-scene-src-file'
            rsv_unit_0 = self._rsv_task.get_rsv_unit(
                keyword=keyword_0, variants_extend=dict(artist=artist)
            )
            rsv_unit_1 = self._rsv_task.get_rsv_unit(
                keyword=keyword_1, variants_extend=dict(artist=artist)
            )
            root_location = rsv_unit_0.get_result()
            if root_location:
                p.set_root(root_location)
                results = rsv_unit_1.get_result(
                    version='all'
                )
                p.set(results)

    def refresh_artist_fnc(self):
        keyword_0 = 'project-user-katana-scene-src-dir'
        rsv_unit_0 = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        result_0 = rsv_unit_0.get_result(version='all')
        if result_0:
            for i_result in result_0:
                i_properties = rsv_unit_0.generate_properties_by_result(i_result)
                i_artist = i_properties.get('artist')
                self._artists.append(i_artist)
        #
        o = self._options_prx_node
        if self._artists:
            v_p = o.get('artist.name')
            o.set('artist.name', self._artists)
            if v_p in self._artists:
                o.set('artist.name', v_p)
            #
            self.refresh_artist_file_fnc()
        else:
            o.set('artist.name', ['None'])

    def refresh_team_fnc(self):
        o = self._options_prx_node
        #
        p = o.get_port('team.file')
        keyword_0 = 'project-source-katana-scene-src-dir'
        rsv_unit_0 = self._rsv_task.get_rsv_unit(
            keyword=keyword_0
        )
        root_location = rsv_unit_0.get_result()
        if root_location:
            p.set_root(root_location)
            self.refresh_team_file_fnc()

    def refresh_team_file_fnc(self):
        o = self._options_prx_node
        #
        p = o.get_port('team.file')
        keyword_1 = 'project-source-katana-scene-src-file'
        rsv_unit_1 = self._rsv_task.get_rsv_unit(
            keyword=keyword_1
        )
        results = rsv_unit_1.get_result(
            version='all'
        )
        p.set(results)

    def refresh_auto_fnc(self):
        o = self._options_prx_node
        self._artists = []
        area = o.get('area')
        if area == 'team':
            self.refresh_team_fnc()
        elif area == 'artist':
            self.refresh_artist_fnc()

    def apply_fnc(self):
        o = self._options_prx_node
        self._artists = []
        area = o.get('area')
        if area == 'team':
            file_paths = o.get('team.file')
        elif area == 'artist':
            file_paths = o.get('artist.file')
        else:
            raise RuntimeError()
        #
        if file_paths:
            # noinspection PyUnresolvedReferences
            ktn_core.GuiNodeGraphOpt.import_nodes_from_file(
                file_paths[0]
            )
