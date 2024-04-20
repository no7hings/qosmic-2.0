# coding:utf-8
import lxgui.core as gui_core

import lxgui.proxy.widgets as prx_widgets


def yes_method():
    import time
    w.set_content('stated')
    print 'AAA'
    # print A
    print w.get_options_as_kwargs()
    time.sleep(5)
    print 'BBB'
    w.add_content('test')
    w.add_content('completed')


if __name__ == '__main__':
    import sys
    #
    from PySide2 import QtWidgets
    #
    app = QtWidgets.QApplication(sys.argv)
    w = prx_widgets.PrxBaseWindow()
    w.set_window_show()
    for i in range(20):
        if i == 10:
            w = gui_core.GuiDialog.create(
                label='label',
                sub_label='sub label',
                yes_method=yes_method,
                use_exec=False,
                options_configure={
                    'user/description/test': {
                        'widget': 'script',
                        'value': u'测试',
                        'enable': False,
                        'tool_tip': '...'
                    }
                },
                window_size=(480, 480),
                status=gui_core.GuiDialog.ValidationStatus.Error,
                parent=w.widget,
                use_window_modality=False,
            )
    #
    sys.exit(app.exec_())
