# coding:utf-8
from qsm_lazy_mtg.gui.abstracts import subpage_for_new_splicing as _subpage_for_new_splicing

import qsm_maya_lazy_mtg.core as qsm_mya_lzy_mtg_core

import qsm_maya_lazy_mtg.scripts as qsm_mya_lzy_mtg_scripts


class PrxSubpageForNewMocapSplicing(_subpage_for_new_splicing.AbsPrxSubpageForNewSplicing):
    GUI_KEY = 'mocap'

    def __init__(self, *args, **kwargs):
        super(PrxSubpageForNewMocapSplicing, self).__init__(*args, **kwargs)

    def _on_apply(self):
        rig_name = self._prx_options_node.get('rig')
        rig_namespace = self._prx_options_node.get('rig_namespace')

        master_layer_name = qsm_mya_lzy_mtg_core.MtgMasterLayer.find_one_master_layer_location(rig_namespace)
        if master_layer_name:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._window._configure.get('build.messages.exists_master_layer')
                )
            )
            return

        scp = qsm_mya_lzy_mtg_scripts.MtgBuildScp(rig_namespace)
        scp.setup_for_mocap(rig_name)

        template = self._prx_options_node.get('template')

        scp.load_template(template)
