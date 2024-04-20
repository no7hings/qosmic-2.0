# coding:utf-8

def main(session):
    def get_asset_tgt(asset_src_):
        return asset_src_

    def yes_method_0():
        raise RuntimeError('this method is removed')

    #
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

    import lxgui.proxy.widgets as prx_widgets

    import lxresolver.core as rsv_core

    resolver = rsv_core.RsvBase.generate_root()
    #
    rsv_asset = session.rsv_obj
    #
    project_src = rsv_asset.get('project')
    asset = rsv_asset.get('asset')
    #
    window_title = 'Pull Asset(s) from "LIB"'
    window_size = 480, 480
    if project_src in ['lib']:
        tree_item = rsv_asset.get_obj_gui()
        tree_view = tree_item.get_view()

        all_items = tree_view.get_all_items()

        assets_src = []
        for i_item in all_items:
            i_rsv_obj = i_item.get_gui_dcc_obj(namespace='resolver')
            if i_rsv_obj:
                if i_rsv_obj.type_name == 'asset':
                    if i_item.get_is_checked() and i_item.get_is_hidden(ancestors=True) is False:
                        assets_src.append(i_rsv_obj.name)
        #
        if assets_src:
            w = gui_core.GuiDialog.create(
                window_title,
                content=(
                    '{} asset(s) is checked:\n'
                    '{}\n'
                    'select a project and press "Yes" to continue...'.format(
                        len(assets_src),
                        ',\n'.join(map(lambda x: '"{}"'.format(x), assets_src))
                    )
                ),
                window_size=window_size,
                yes_method=yes_method_0,
                show=False,
                use_exec=False
            )
            w.set_options_group_enable()
            #
            p = w._options_prx_node.add_port(
                prx_widgets.PrxPortAsConstantChoose(
                    'project', 'Project'
                )
            )
            projects = get_projects()
            p.set(enumerate_strings=projects)
            #
            w.set_window_show()
        else:
            gui_core.GuiDialog.create(
                'Push Asset(s) to "LIB"',
                content='no asset(s) has checked',
                status=gui_core.GuiDialog.ValidationStatus.Error
            )
    else:
        gui_core.GuiDialog.create(
            window_title,
            content='project "{}" is not supported...'.format(project_src),
            status=gui_core.GuiDialog.ValidationStatus.Error
        )


# noinspection PyUnresolvedReferences
main(session)
