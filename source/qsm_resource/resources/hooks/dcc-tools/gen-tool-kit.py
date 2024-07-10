# coding:utf-8

def main(session):
    import lxtool.kit.gui.widgets as kit_gui_widgets

    kit_gui_widgets.DccToolKit(session).show_window_auto()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
