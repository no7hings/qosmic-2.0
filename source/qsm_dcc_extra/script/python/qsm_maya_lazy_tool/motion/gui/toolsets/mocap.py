# coding:utf-8
import lxbasic.core as bsc_core

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_maya.core as qsm_mya_core

import qsm_maya.adv as qsm_mya_adv


class PrxToolsetForMoCapImport(gui_prx_widgets.PrxBaseUnit):
    GUI_KEY = 'import_mocap'

    def do_dcc_import_character_mocap_to_control(self):
        locations = qsm_mya_core.Selection.get()
        if len(locations) >=2:
            location_0, location_1 = locations[:2]
            rig_namespace = qsm_mya_core.Namespace.extract_from_path(location_0)
            if qsm_mya_adv.AdvOpt.check_is_valid(rig_namespace) is False:
                self._window.exec_message_dialog(
                    self.choice_gui_message(
                        self._page._configure.get('build.messages.no_selection')
                    ),
                    status='warning'
                )
                return

            path_opt = bsc_core.BscNodePathOpt(location_1)

            mocap_location = None
            comps = path_opt.get_components()
            for i_path_opt in comps:
                if i_path_opt.has_namespace():
                    i_result = i_path_opt.is_name_match_pattern('*:Hips')
                else:
                    i_result = i_path_opt.is_name_match_pattern('Hips')

                if i_result is True:
                    mocap_location = i_path_opt.get_path()
                    break

            if not mocap_location:
                self._window.exec_message_dialog(
                    self.choice_gui_message(
                        self._page._configure.get('build.messages.no_selection')
                    ),
                    status='warning'
                )
                return

            import qsm_maya_lazy_montage.core.transfer.handle as h

            h.MocapToAdvHandle(
                rig_namespace, mocap_location=mocap_location
            ).execute()
        else:
            self._window.exec_message_dialog(
                self.choice_gui_message(
                    self._page._configure.get('build.messages.no_selection')
                ),
                status='warning'
            )
            return

    def __init__(self, window, page, session):
        super(PrxToolsetForMoCapImport, self).__init__(window, page, session)

        self.gui_unit_setup_fnc()

    def gui_unit_setup_fnc(self):
        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            self.choice_gui_name(
                self._page._configure.get('build.units.{}.options'.format(self.GUI_KEY))
            )
        )

        self._prx_options_node.build_by_data(
            self._page._configure.get(
                'build.units.{}.options.parameters'.format(self.GUI_KEY)
            ),
        )

        prx_sca = gui_prx_widgets.PrxVScrollArea()
        prx_sca.add_widget(self._prx_options_node)

        self._qt_layout.addWidget(prx_sca.widget)

        self._prx_options_node.set(
            'character_mocap.to_control', self.do_dcc_import_character_mocap_to_control
        )
