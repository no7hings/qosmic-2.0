# coding:utf-8
from lnx_resora.gui import abstracts as lnx_rsr_abstracts

from .. import scripts as _script


class PrxSubpageForRegister(lnx_rsr_abstracts.AbsPrxSubpageForVideoRegister):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(PrxSubpageForRegister, self).__init__(window, session, subwindow, *args, **kwargs)

    def _on_apply(self):
        prx_node = self._prx_options_node

        file_paths = prx_node.get('files')

        scr_type_paths = self.gui_get_scr_type_paths()
        scr_tag_paths = self.gui_get_scr_tag_paths()

        collect_source = prx_node.get('collect_source')

        if file_paths:
            _script.VideoRegisterBatch(
                self._scr_stage.key, file_paths, collect_source
            ).execute(
                scr_type_paths, scr_tag_paths
            )

            scr_type_paths_addition = self._get_scr_type_or_tag_paths_addition(self._type_qt_tag_widget)
            scr_tag_paths_addition = self._get_scr_type_or_tag_paths_addition(self._tag_qt_tag_widget)

            if self._post_fnc is not None:
                # if scr_type_paths_addition or scr_tag_paths_addition:
                # update always
                self._post_fnc(scr_type_paths_addition, scr_tag_paths_addition)

            self._subwindow.popup_message(
                self._subwindow.choice_gui_message(
                    self._configure.get('build.messages.register_successful')
                )
            )

        prx_node.get_port('files').do_clear()

        self.clear_type_and_tag_checked()