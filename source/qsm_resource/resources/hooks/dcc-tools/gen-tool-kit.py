# coding:utf-8

def main(session):
    import lxtool.kit.gui.widgets as kit_gui_widgets

    kit_gui_widgets.DccToolKit(session).set_window_show()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
