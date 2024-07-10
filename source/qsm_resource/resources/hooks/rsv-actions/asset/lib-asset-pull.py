# coding:utf-8

def main(session):
    def ok_method_0():
        def ok_method_1():
            raise RuntimeError('this method is removed')
        #
        _kwargs = w.get_options_as_kwargs()
        _project_tgt = _kwargs['project']
        _asset_tgt = asset_src
        #
        _rsv_asset_tgt = resolver.get_rsv_resource(
            project=_project_tgt, asset=asset_src
        )
        if _rsv_asset_tgt is not None:
            gui_core.GuiDialog.create(
                window_title,
                content=(
                    'asset:\n'
                    '"{}"\n'
                    'asset is already exists\n'
                    'do you want to override exists...'
                ).format(
                    _asset_tgt
                ),
                ok_method=ok_method_1,
                ok_label='Override',
                no_label='Don\'t Override',
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                use_exec=False
            )
        else:
            ok_method_1()

    def get_projects():
        lis = []
        shotgun_connector = session.get_shotgun_connector()
        for stg_project_query in shotgun_connector.get_stg_project_queries():
            if stg_project_query.get('sg_studio') in ['CG']:
                name = stg_project_query.get('tank_name')
                if name:
                    lis.append(name)
        #
        lis.sort()
        return lis

    import lxgui.core as gui_core

    import lxgui.proxy.widgets as gui_prx_widgets

    import lxresolver.core as rsv_core

    resolver = rsv_core.RsvBase.generate_root()

    rsv_entity = session.rsv_obj

    project = rsv_entity.get('project')
    asset_src = rsv_entity.get('asset')

    window_title = 'Pull Asset from "LIB"'
    if project in ['lib']:
        w = gui_core.GuiDialog.create(
            window_title,
            content=(
                'asset:\n'
                '"{}"\n'
                'select a project and press "Ok" to continue...'.format(
                    asset_src
                )
            ),
            ok_method=ok_method_0,
            show=False,
            use_exec=False
        )
        w.set_options_group_enable()
        #
        p = w._options_prx_node.add_port(
            gui_prx_widgets.PrxPortAsConstantChoose(
                'project', 'Project'
            )
        )
        projects = get_projects()
        p.set(enumerate_strings=projects)
        #
        w.show_window_auto()
    else:
        gui_core.GuiDialog.create(
            window_title,
            content='project "{}" is not supported...'.format(project),
            status=gui_core.GuiDialog.ValidationStatus.Error
        )


# noinspection PyUnresolvedReferences
main(session)

