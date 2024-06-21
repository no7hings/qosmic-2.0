# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.proxy.widgets as gui_prx_widgets


class PnlUsdFormatConvert(gui_prx_widgets.PrxSessionToolWindow):
    IMAGE_KEYS = [
        'preview'
    ]
    TEXTURE_KEYS = [
        'albedo',
        'diffuse',
        'ao',
        'specular',
        'roughness', 'glossiness',
        'coat',
        'coat_roughness',
        'opacity',
        'normal',
        'displacement',
        #
        'mask'
    ]

    def apply_fnc(self):
        file_path_src = self._options_prx_node.get('from')
        file_path_tgt = self._options_prx_node.get('to')
        file_opt_src = bsc_storage.StgFileOpt(file_path_src)
        if file_opt_src.get_is_file() is True:
            cmd = 'rez-env usd -- usdcat -o {} {}'.format(
                file_path_tgt, file_path_src
            )
            bsc_core.PrcBaseMtd.execute_with_result(
                cmd
            )

    def gui_setup_window(self):
        s_0 = gui_prx_widgets.PrxVScrollArea()
        self.add_widget(s_0)
        h_s = gui_prx_widgets.PrxHSplitter()
        s_0.add_widget(h_s)
        #
        s_1 = gui_prx_widgets.PrxVScrollArea()
        h_s.add_widget(s_1)
        #
        self._options_prx_node = gui_prx_widgets.PrxOptionsNode('options')
        s_1.add_widget(self._options_prx_node)
        self._options_prx_node.build_by_data(
            self._session.configure.get('build.node.options'),
        )
        #
        self._tip_prx_text_browser = gui_prx_widgets.PrxTextBrowser()
        s_1.add_widget(self._tip_prx_text_browser)
        self._tip_prx_text_browser.set_font_size(12)
        self._tip_prx_text_browser.set_content(
            self._session.configure.get('build.node.content'),
        )

    def __init__(self, session, *args, **kwargs):
        super(PnlUsdFormatConvert, self).__init__(session, *args, **kwargs)


def main(session):
    import lxgui.proxy.core as gui_prx_core

    gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
        PnlUsdFormatConvert, session=session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
