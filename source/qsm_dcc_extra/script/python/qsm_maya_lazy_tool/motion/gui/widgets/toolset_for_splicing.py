# coding:utf-8
import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_maya.core as qsm_mya_core

import qsm_maya.tasks.animation.core as qsm_mya_tsk_anm_core

import qsm_maya.adv.core as qsm_mya_adv_core


class PrxToolsetForImportMotion(gui_prx_widgets.PrxBaseUnit):
    UNIT_KEY = 'import_motion'

    def get_dcc_character_args(self):
        results = []
        namespaces = qsm_mya_core.Namespaces.extract_from_selection()
        if namespaces:
            results = qsm_mya_tsk_anm_core.AdvRigAsset.filter_namespaces(namespaces)

        if not results:
            self._window.exec_message_dialog(
                self._window.choice_message(
                    self._window._configure.get('build.main.messages.no_characters')
                ),
                status='warning'
            )
            return
        return results

    def do_dcc_import_character_motion_to_control(self):
        namespaces = self.get_dcc_character_args()
        if namespaces:
            file_path = gui_core.GuiStorageDialog.open_file(
                ext_filter='All File (*.jsz)', parent=self._window._qt_widget
            )
            if file_path:
                with self._window.gui_progressing(
                    maximum=len(namespaces), label='import motion to characters'
                ) as g_p:
                    for i_namespace in namespaces:
                        i_opt = qsm_mya_adv_core.AdvChrOpt(i_namespace)
                        i_opt.load_controls_motion_from(
                            file_path,
                            force=True,
                            frame_offset=0,
                        )
                        g_p.do_update()

            self._window.popup_message(
                self._window.choice_message(
                    self._window._configure.get(
                        'build.{}.messages.import_characters'.format(self._page.PAGE_KEY)
                    )
                )
            )

    def __init__(self, window, page, session):
        super(PrxToolsetForImportMotion, self).__init__(window, page, session)

        self.gui_unit_setup_fnc()

    def gui_unit_setup_fnc(self):
        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_name(
                self._window._language, self._window._configure.get(
                    'build.{}.units.{}.options'.format(
                        self._page.PAGE_KEY, self.UNIT_KEY
                    )
                )
            )
        )

        self._prx_options_node.build_by_data(
            self._window._configure.get(
                'build.{}.units.{}.options.parameters'.format(
                    self._page.PAGE_KEY, self.UNIT_KEY
                )
            ),
        )

        prx_sca = gui_prx_widgets.PrxVScrollArea()
        prx_sca.add_widget(self._prx_options_node)

        self._qt_layout.addWidget(prx_sca.widget)

        self._prx_options_node.set(
            'import_character_motion.to_control', self.do_dcc_import_character_motion_to_control
        )
