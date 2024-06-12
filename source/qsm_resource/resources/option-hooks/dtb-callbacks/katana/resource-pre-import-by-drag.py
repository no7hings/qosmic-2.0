# coding:utf-8


def main(session):
    import lxkatana.core as ktn_core

    dtb_opt = session.get_database_opt()
    if dtb_opt:
        window = session.get_window()
        #
        dtb_resource = dtb_opt.get_entity(
            entity_type=session.option_opt.get('entity_type'),
            filters=[
                ('path', 'is', session.option_opt.get('entity'))
            ]
        )

        resource_path = dtb_resource.path
        gui_resource_opt = window.get_gui_resource_opt()
        prx_item = gui_resource_opt.gui_get_one(resource_path)

        mime_data = prx_item.get_drag_mime_data()

        tab_opt = ktn_core.GuiNodeGraphTabOpt()
        ktn_group = tab_opt.get_current_group()
        if ktn_group:
            ktn_group_opt = ktn_core.NGNodeOpt(ktn_group)
            mime_data.setData('nodegraph/noderefs', ktn_group_opt.get_name())


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
