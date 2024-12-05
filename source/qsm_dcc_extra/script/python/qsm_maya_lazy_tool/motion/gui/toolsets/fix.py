# coding:utf-8
import lxgui.core as gui_core

import lxgui.proxy.widgets as gui_prx_widgets

import qsm_maya.core as qsm_mya_core

import qsm_maya.handles.animation.core as qsm_mya_hdl_anm_core

import qsm_maya.motion.core as qsm_mya_mtn_core


class PrxToolsetReferenceFix(gui_prx_widgets.PrxBaseUnit):
    GUI_KEY = 'reference_fix'

    @qsm_mya_core.Undo.execute
    def _on_recover_lost_anm_curve(self):
        reference_nodes = qsm_mya_core.ReferencesCache().find_from_selection()
        if not reference_nodes:
            self._window.exec_message_dialog(
                self._window.choice_gui_message(
                    self._window._configure.get('build.{}.messages.no_references'.format(self._page.GUI_KEY))
                ),
                status='warning'
            )

        namespaces = qsm_mya_core.Namespaces.extract_from_selection()
        if namespaces:
            for i_reference_node in reference_nodes:
                qsm_mya_mtn_core.ReferenceFix(i_reference_node).fix_placeholder()

    def __init__(self, window, page, session):
        super(PrxToolsetReferenceFix, self).__init__(window, page, session)

        self.gui_unit_setup_fnc()

    def gui_unit_setup_fnc(self):
        self._prx_options_node = gui_prx_widgets.PrxOptionsNode(
            gui_core.GuiUtil.choice_gui_name(
                self._window._language, self._window._configure.get(
                    'build.{}.units.{}.options'.format(
                        self._page.GUI_KEY, self.GUI_KEY
                    )
                )
            )
        )

        self._prx_options_node.build_by_data(
            self._window._configure.get(
                'build.{}.units.{}.options.parameters'.format(
                    self._page.GUI_KEY, self.GUI_KEY
                )
            ),
        )

        prx_sca = gui_prx_widgets.PrxVScrollArea()
        prx_sca.add_widget(self._prx_options_node)

        self._qt_layout.addWidget(prx_sca.widget)

        self._prx_options_node.set(
            'anm_curve.recover_lost', self._on_recover_lost_anm_curve
        )
