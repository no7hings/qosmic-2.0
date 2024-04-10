# coding:utf-8
import lxgui.proxy.widgets as prx_widgets


class PnlClearnerForScene(prx_widgets.PrxSessionToolWindow):
    def __init__(self, session, *args, **kwargs):
        super(PnlClearnerForScene, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):
        self._options_prx_node = prx_widgets.PrxNode('options')
        self.add_widget(self._options_prx_node)
        self._options_prx_node.create_ports_by_data(
            self._session.configure.get('build.node.options'),
        )

    def apply_fnc(self):
        ps = [i_p for i_p in self._options_prx_node.get_ports() if i_p.get_type() == 'check_button' and i_p]
        if ps:
            with self.gui_progressing(maximum=len(ps), label='clean all') as g_p:
                for i_p in ps:
                    g_p.do_update()
                    #
                    i_p.execute()
