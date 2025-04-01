# coding:utf-8
from lnx_montage.gui.abstracts import subpage_for_new_splicing as _subpage_for_adv

import qsm_maya.core as qsm_mya_core

import qsm_maya.adv as qsm_mya_adv

import lnx_maya_montage.core as qsm_mya_lzy_mtg_core

import lnx_maya_montage.scripts as qsm_mya_lzy_mtg_scripts


class PrxSubpageForNewGeneralSplicing(_subpage_for_adv.AbsPrxSubpageForNewSplicing):
    GUI_KEY = 'general'

    def __init__(self, *args, **kwargs):
        super(PrxSubpageForNewGeneralSplicing, self).__init__(*args, **kwargs)

    def _on_apply(self):
        rig_scheme = self._prx_options_node.get('rig_scheme')
        if rig_scheme == 'adv':
            self._create_for_adv()
        elif rig_scheme == 'mocap':
            self._create_for_mocap()

    def _create_for_adv(self):
        rig_namespace = self._prx_options_node.get('adv_rig_namespace')

        if not rig_namespace:
            return

        master_layer_name = qsm_mya_lzy_mtg_core.MtgMasterLayer.find_one_master_layer_location(rig_namespace)
        if master_layer_name:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._window._configure.get('build.messages.exists_master_layer')
                )
            )
            return

        scp = qsm_mya_lzy_mtg_scripts.MtgBuildScp(rig_namespace)
        scp.setup_for_adv()

        template = self._prx_options_node.get('template')

        scp.load_template(template)

    def _create_for_mocap(self):
        rig_name = self._prx_options_node.get('mocap_rig')
        rig_namespace = self._prx_options_node.get('mocap_rig_namespace')

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

    def gui_refresh_adv_rig_namespaces(self):
        rig_namespaces = []

        namespaces = qsm_mya_core.Namespaces.get_all()
        for i in namespaces:
            if qsm_mya_adv.AdvOpt.check_is_valid(i):
                rig_namespaces.append(i)

        valid_rig_namespace = qsm_mya_lzy_mtg_core.MtgStage.find_all_valid_rig_namespaces()

        options = [x for x in rig_namespaces if x not in valid_rig_namespace]

        port = self._prx_options_node.get_port('adv_rig_namespace')
        if options:
            port.set_options(options)
            port.set(options[0])
        else:
            port.set_options([])

    def do_gui_refresh_all(self):
        self.gui_refresh_adv_rig_namespaces()
