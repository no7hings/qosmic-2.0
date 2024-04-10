# coding:utf-8
import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.qt.core as gui_qt_core

import lxgui.qt.widgets as qt_widgets

import lxgui.proxy.widgets as prx_widgets


class AbsPnlLauncherForApplication(prx_widgets.PrxSessionWindow):
    KEY = 'launcher'

    def __init__(self, session, *args, **kwargs):
        super(AbsPnlLauncherForApplication, self).__init__(session, *args, **kwargs)

    def set_all_setup(self):

        self._sub_label = qt_widgets.QtTextItem()
        self.add_widget(self._sub_label)
        self._sub_label.setFixedHeight(20)
        self._sub_label._set_name_draw_font_(gui_qt_core.QtFonts.SubTitle)
        self._sub_label._set_name_text_option_to_align_center_()

        self.__input = prx_widgets.PrxInputAsStgTask()
        self.add_widget(self.__input)

        self.__input.set_focus_in()

        self.get_widget().key_escape_pressed.connect(
            self.__do_cancel
        )

        self.__tip = prx_widgets.PrxTextBrowser()
        self.add_widget(self.__tip)
        self.__tip.set_focus_enable(False)

        self.__next_button = prx_widgets.PrxPressItem()
        self.__next_button.set_name('next')
        self.add_button(
            self.__next_button
        )
        self.__next_button.connect_press_clicked_to(self.__do_next)

        self.__next_button.set_enable(False)

        self.__input.connect_result_to(self.__do_accept)
        self.__input.connect_tip_trace_to(self.__do_tip_accept)

        self.__input.setup()

        self.__application = 'maya'

        self.__set_application(
            self._session.configure.get('option.extend.application')
        )

    def __set_application(self, application):
        self.__application = application
        self._sub_label._set_name_text_(application)

    def __get_application(self):
        return self.__application

    def __do_accept(self, dict_):
        if dict_:
            option_opt = bsc_core.ArgDictStringOpt(dict_)
            option_opt.set('application', self.__get_application())
            option = option_opt.to_string()

            if bsc_core.SysBaseMtd.get_is_linux():
                cmd = bsc_storage.PkgContextNew(
                    ' '.join(['lxdcc'])
                ).get_command(
                    args_execute=[
                        '-- lxapp -o \\\"{}\\\"'.format(
                            option
                        )
                    ],
                )
            elif bsc_core.SysBaseMtd.get_is_windows():
                cmd = bsc_storage.PkgContextNew(
                    ' '.join(['lxdcc'])
                ).get_command(
                    args_execute=[
                        '-- lxapp -o "{}"'.format(
                            bsc_core.PrcBaseMtd._cmd_cleanup(option)
                        )
                    ],
                )
            else:
                raise RuntimeError()

            bsc_core.ExcExtraMtd.execute_shell_script_use_terminal(
                '"{}"'.format(cmd), **dict(title='{}-{}'.format(self.__get_application(), bsc_core.SysBaseMtd.get_time_tag()))
            )
            self.close_window_later()

    def __do_next(self):
        self.__do_accept(self.__input.get_result())

    def __do_tip_accept(self, text):
        if self.__input.get_is_valid():
            self.__next_button.set_enable(True)
        else:
            self.__next_button.set_enable(False)

        self.__tip.set_content(text)

    def __do_cancel(self):
        if self.__input.has_focus() is False:
            self.close_window_later()
