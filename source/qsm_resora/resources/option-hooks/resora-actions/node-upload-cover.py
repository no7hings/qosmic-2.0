# coding:utf-8
import lxgui.core as gui_core


@gui_core.Verify.execute('resora', 7)
def main(session):
    window = session.find_window()
    if not window:
        return

    import lnx_screw.core as c

    option_opt = session.option_opt
    scr_stage_name = option_opt.get('stage_name')
    scr_entity_path = option_opt.get('entity')
    scr_stage = c.Stage(scr_stage_name)

    scr_entity = scr_stage.get_node(scr_entity_path)
    if scr_entity:
        image_path = gui_core.GuiStorageDialog.open_file(
            ext_filter='All File (*.jpg *.png)', parent=window._qt_widget
        )

        if image_path:
            result = scr_stage.upload_node_preview(scr_entity_path, image_path)
            if result is True:
                page = window.gui_get_current_page()
                page._gui_node_opt.gui_reload_entity(scr_entity_path, update_thumbnail=True)
            else:
                window.exec_message_dialog(
                    'Upload image failed.',
                    status='error'
                )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
