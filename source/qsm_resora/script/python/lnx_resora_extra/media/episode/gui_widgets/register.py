# coding:utf-8
from lnx_resora.gui import abstracts as lnx_rsr_gui_abstracts

from .. import scripts as _scripts


class GuiResourceRegisterMain(lnx_rsr_gui_abstracts.AbsPrxPageForAnyRegister):
    def __init__(self, *args, **kwargs):
        super(GuiResourceRegisterMain, self).__init__(*args, **kwargs)

    def _update_history_options(self):
        for i in [
            'directory',
            'file.pattern',
            'auto_class.enable',
            'auto_class.file_pattern',
            'auto_class.type_pattern',
            'collect_source',
        ]:
            i_p = self._prx_options_node.get_port(i)
            i_p.set_history_group(['resora', self._scr_stage.key])
            i_p.pull_history_latest()

    def _on_apply(self):
        prx_node = self._prx_options_node

        directory_path = prx_node.get('directory')
        file_pattern = prx_node.get('file.pattern')
        file_formats = prx_node.get('file.formats')

        with_auto_class = prx_node.get('auto_class.enable')
        auto_class_file_pattern = prx_node.get('auto_class.file_pattern')
        auto_class_type_pattern = prx_node.get('auto_class.type_pattern')

        collect_source = prx_node.get('collect_source')
        
        scr_type_paths = self.gui_get_scr_type_paths()
        scr_tag_paths = self.gui_get_scr_tag_paths()

        _scripts.EpisodeRegisterBatch.register_fnc(
            self._scr_stage.key, directory_path,
            file_pattern=file_pattern, file_formats=file_formats,
            with_auto_class=with_auto_class, auto_class_file_pattern=auto_class_file_pattern,
            auto_class_type_pattern=auto_class_type_pattern,
            collect_source=collect_source,
            scr_type_paths=scr_type_paths, scr_tag_paths=scr_tag_paths
        )


