# coding:utf-8


def main(session):
    import lxtool.submitter.gui.widgets as smt_gui_widgets

    file_path = session.rsv_unit.get_result(
        version='latest'
    )
    if file_path:
        hook_option = 'file={}'.format(file_path)
        w = smt_gui_widgets.PnlSubmitterForShotRender(hook_option=hook_option)
        w.show_window_auto()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
