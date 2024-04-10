# coding:utf-8
import lxbasic.core as bsc_core
# gui
from . import configure as gui_cor_configure


class GuiDialog(object):
    ValidationStatus = gui_cor_configure.GuiValidationStatus

    # noinspection PyUnusedLocal
    @classmethod
    def create(
        cls,
        label,
        sub_label=None,
        content=None,
        content_text_size=10,
        window_size=(480, 160),
        yes_method=None,
        yes_label=None,
        yes_visible=True,
        #
        no_method=None,
        no_label=None,
        no_visible=True,
        #
        cancel_fnc=None,
        cancel_label=None,
        cancel_visible=True,
        #
        tip_visible=True,
        #
        button_size=160,
        status=None,
        use_as_error=False,
        use_as_warning=False,
        show=True,
        use_exec=True,
        options_configure=None,
        use_thread=False,
        parent=None,
        #
        use_window_modality=True
    ):
        from ..proxy import widgets as prx_widgets

        if use_exec is True:
            w = prx_widgets.PrxDialogWindow1(parent=parent)
        else:
            w = prx_widgets.PrxDialogWindow0(parent=parent)
        #
        w.set_window_modality(use_window_modality)
        #
        w.set_use_thread(use_thread)
        w.set_window_title(label)
        #
        if sub_label is not None:
            w.set_sub_label(sub_label)
        #
        if content is not None:
            w.set_content(content)
        #
        w.set_content_font_size(content_text_size)
        w.set_definition_window_size(window_size)
        if yes_label is not None:
            w.set_yes_label(yes_label)
        if yes_method is not None:
            w.connect_yes_to(yes_method)
        w.set_yes_visible(yes_visible)
        #
        if no_label is not None:
            w.set_no_label(no_label)
        if no_method is not None:
            w.connect_no_to(no_method)
        w.set_no_visible(no_visible)
        #
        if cancel_label is not None:
            w.set_cancel_label(cancel_label)
        if cancel_fnc is not None:
            w.connect_cancel_method(cancel_fnc)
        w.set_cancel_visible(cancel_visible)
        #
        if status is not None:
            w.set_window_title(label)
            w.set_status(status)
        #
        if options_configure is not None:
            w.set_options_group_enable()
            w.set_options_create_by_configure(options_configure)
        #
        w.set_tip_visible(tip_visible)
        #
        if show is True:
            w.set_window_show()
        return w


class GuiDialogForChooseAsBubble(object):
    @classmethod
    def create(cls, texts, tips):
        from ..qt import core as gui_qt_core

        from ..qt import widgets as qt_widgets

        parent = gui_qt_core.GuiQtDcc.get_qt_main_window()
        if parent is not None:
            w = qt_widgets.QtBubbleAsChoose(parent)
            w._set_texts_(texts)
            w._set_tips_(tips)
            w._do_popup_start_()
            return w
        return None


class GuiDialogForFile(object):
    @classmethod
    def open_file(cls, ext_filter='All File (*.*)', parent=None):
        from ..qt import core as gui_qt_core

        dlg = gui_qt_core.QtWidgets.QFileDialog()
        options = dlg.Options()
        # options |= dlg.DontUseNativeDialog
        r = dlg.getOpenFileName(
            parent,
            'Open File',
            filter=ext_filter,
            options=options,
        )
        if r:
            _ = r[0]
            if _:
                return _
        return None

    @classmethod
    def save_file(cls, ext_filter='All File (*.*)', parent=None):
        from ..qt import core as gui_qt_core

        dlg = gui_qt_core.QtWidgets.QFileDialog()
        options = dlg.Options()
        # options |= dlg.DontUseNativeDialog
        r = dlg.getSaveFileName(
            parent,
            'Save File',
            '',
            filter=ext_filter,
            options=options,
        )
        if r:
            _ = r[0]
            if _:
                return _
        return None

    @classmethod
    def open_directory(cls, parent=None):
        from ..qt import core as gui_qt_core

        dlg = gui_qt_core.QtWidgets.QFileDialog()
        options = dlg.Options()
        # options |= dlg.DontUseNativeDialog
        r = dlg.getExistingDirectory(
            parent,
            'Open Directory',
            '',
            options=options,
        )
        if r:
            return r
        return None

    @classmethod
    def save_directory(cls, parent=None):
        from ..qt import core as gui_qt_core

        dlg = gui_qt_core.QtWidgets.QFileDialog()
        options = dlg.Options()
        # options |= dlg.DontUseNativeDialog
        r = dlg.getExistingDirectory(
            parent,
            'Save Directory',
            '',
            options=options,
        )
        if r:
            return r
        return None


class GuiMonitorForDeadline(object):
    @classmethod
    def set_create(cls, label, job_id, parent=None):
        import lxbasic.deadline as bsc_deadline

        from ..proxy import widgets as prx_widgets

        w = prx_widgets.PrxMonitorWindow(parent=parent)
        w.set_window_title(
            '{}({})'.format(
                label, job_id
            )
        )
        button = w.get_status_button()
        j_m = bsc_deadline.DdlJobMonitor(job_id)
        button.set_statuses(j_m.get_task_statuses())
        button.set_initialization(j_m.get_task_count())
        j_m.logging.connect_to(w.set_logging)
        j_m.task_status_changed_at.connect_to(w.set_status_at)
        j_m.task_finished_at.connect_to(w.set_finished_at)
        j_m.set_start()

        w.connect_window_close_to(j_m.set_stop)

        w.set_window_show(size=(480, 240))


class GuiMonitorForCommand(object):
    @classmethod
    def set_create(cls, label, command, parent=None):
        # noinspection PyUnusedLocal
        def completed_fnc_(*args):
            w.set_status(w.ValidationStatus.Correct)
            w.close_window_later()

        # noinspection PyUnusedLocal
        def failed_fnc_(*args):
            w.set_status(w.ValidationStatus.Error)

        # noinspection PyUnusedLocal
        def finished_fnc_(*args):
            pass

        from ..qt import core as gui_qt_core

        from ..proxy import widgets as prx_widgets

        w = prx_widgets.PrxMonitorWindow(parent=parent)
        w.set_window_title(label)
        #
        status_button = w.get_status_button()
        c_t = bsc_core.TrdCommand(command)
        status_button.set_statuses([c_t.get_status()])
        status_button.set_initialization(1)
        c_t.status_changed.connect_to(lambda x: w.set_status_at(0, x))
        # c_t.finished.connect_to(lambda x: w.set_finished_at(0, x))
        c_t.logging.connect_to(w.set_logging)
        w.connect_window_close_to(c_t.set_stopped)
        #
        q_c_s = gui_qt_core.QtCommandSignals(w.widget)
        #
        c_t.completed.connect_to(q_c_s.completed.emit)
        c_t.finished.connect_to(q_c_s.finished.emit)
        c_t.failed.connect_to(q_c_s.failed.emit)
        #
        q_c_s.completed.connect(completed_fnc_)
        q_c_s.failed.connect(failed_fnc_)
        q_c_s.finished.connect(finished_fnc_)
        #
        c_t.start()

        w.set_window_show(size=(480, 240))
        return q_c_s
