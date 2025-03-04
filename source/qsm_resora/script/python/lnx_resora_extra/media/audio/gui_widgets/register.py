# coding:utf-8
from lnx_resora.gui import abstracts as lnx_rsr_abstracts

from .. import scripts as _scripts


class PrxSubpageForRegister(lnx_rsr_abstracts.AbsPrxSubpageForAudioRegister):
    def __init__(self, window, session, subwindow, *args, **kwargs):
        super(PrxSubpageForRegister, self).__init__(window, session, subwindow, *args, **kwargs)

    def _on_apply(self):
        prx_node = self._prx_options_node

        file_paths = prx_node.get('files')

        scr_type_paths = self.gui_get_scr_type_paths()
        scr_tag_paths = self.gui_get_scr_tag_paths()

        collect_source = prx_node.get('collect_source')

        if file_paths:
            _scripts.AudioRegisterBatch(
                self._scr_stage.key, file_paths, collect_source
            ).execute(scr_type_paths, scr_tag_paths)

            self._subwindow.popup_message(
                self._subwindow.choice_gui_message(
                    self._configure.get('build.messages.register_successful')
                )
            )

        prx_node.get_port('files').do_clear()

        self.clear_type_and_tag_checked()
