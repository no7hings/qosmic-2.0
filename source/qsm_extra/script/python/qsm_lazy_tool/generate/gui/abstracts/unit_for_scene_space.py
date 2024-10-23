# coding:utf-8
import lxgui.proxy.widgets as gui_prx_widgets


class AbsPrxUnitForSceneSpace(gui_prx_widgets.PrxBaseUnit):
    def __init__(self, window, page, session):
        super(AbsPrxUnitForSceneSpace, self).__init__(window, page, session)

        self.gui_unit_setup_fnc()

    def gui_unit_setup_fnc(self):
        self._scene_prx_scene_view = gui_prx_widgets.PrxSceneView()
        self._qt_layout.addWidget(self._scene_prx_scene_view.widget)

        self._scene_prx_scene_view.set_scene_ext(
            '.ma'
        )
        self._scene_prx_scene_view.set_root(
            'Z:/temporaries/nothings/montage'
        )
        
    def update_scene_view(self):
        self._scene_prx_scene_view.update()

    def set_scene_gain_fnc(self, fnc):
        self._scene_prx_scene_view.set_scene_gain_fnc(
            fnc
        )

    def connect_open_scene_to(self, fnc):
        self._scene_prx_scene_view.connect_open_scene_to(
            fnc
        )

    def connect_save_scene_to(self, fnc):
        self._scene_prx_scene_view.connect_save_scene_to(
            fnc
        )




