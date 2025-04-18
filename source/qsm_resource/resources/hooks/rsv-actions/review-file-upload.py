# coding:utf-8
import lxbasic.log as bsc_log

import lxgui.proxy.widgets as gui_prx_widgets


class UploadReview(gui_prx_widgets.PrxBaseWindow):
    def __init__(self, *args, **kwargs):
        super(UploadReview, self).__init__(*args, **kwargs)


def ok_method():
    w = UploadReview()
    w.show_window_auto()


@bsc_log.LogDebug.run
def main(session):
    import lxgui.core as gui_core

    rsv_task = session.rsv_obj
    branch = rsv_task.get('branch')
    #
    window_title = 'Upload Review'
    #
    rsv_task_version_unit = rsv_task.get_rsv_unit(
        keyword='{}-release-version-dir'.format(branch)
    )
    #
    version = rsv_task_version_unit.get_new_version()
    kwargs = rsv_task.properties.get_value_as_copy()
    kwargs['version'] = version
    if branch == 'asset':
        content = (
            'upload review to\n'
            'version: "{asset}.{step}.{task}.{version}"\n'
            'press "Ok" to continue...'
        ).format(
            **kwargs
        )
    elif branch == 'shot':
        content = (
            'upload review to\n'
            'version: "{shot}.{step}.{task}.{version}"\n'
            'press "Ok" to continue...'
        ).format(
            **kwargs
        )
    else:
        raise TypeError()

    w = gui_core.GuiDialog.create(
        window_title,
        content=content,
        ok_method=ok_method,
        window_size=(480, 320),
        use_exec=False
    )
    # w.set_options_group_enable()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
