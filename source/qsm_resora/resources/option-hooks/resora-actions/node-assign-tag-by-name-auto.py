# coding:utf-8
import lxgui.core as gui_core


class Main(object):
    def __init__(self, session):
        self._session = session
        self._option_opt = self._session.option_opt

    @gui_core.Verify.execute('resora-secondary', 7)
    def execute(self):
        window = self._session.find_window()
        if window is not None:
            import lxbasic.pinyin as bsc_pinyin

            import lnx_screw.core as scr_core

            scr_stage_name = self._option_opt.get('stage_name')

            scr_stage = scr_core.Stage(scr_stage_name)

            page = window.gui_get_current_page()
            gui_node_opt = page._gui_node_opt
            scr_entities = gui_node_opt.gui_get_checked_or_selected_scr_entities()
            if not scr_entities:
                window.exec_message_dialog(
                    'Check or select one or more items and continue.'
                )
                return

            result = window.exec_message_dialog(
                'Create tag assigns by name, press "Ok" to continue.',
                title='Create Assign',
                status='warning',
                show_cancel=True,
            )
            if result:
                tag_map = scr_stage.generate_tag_map('chs')
                if tag_map and scr_entities:
                    for i in scr_entities:
                        i_node_path = i.path
                        i_name = i.gui_name_chs
                        i_keys = bsc_pinyin.Text.split(i_name)
                        for j_key in i_keys:
                            if j_key in tag_map:
                                j_tag_paths = tag_map[j_key]
                                for k_tag_path in j_tag_paths:
                                    scr_stage.create_node_tag_assign(
                                        i_node_path, k_tag_path
                                    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    Main(session).execute()
