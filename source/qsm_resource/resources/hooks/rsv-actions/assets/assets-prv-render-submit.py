# coding:utf-8


def main(session):
    def ok_method():
        for i in assets:
            _i_rsv_task = rsv_project.get_rsv_task(
                asset=i, step='mod', task='modeling'
            )

            i_work_scene_src_rsv_unit = _i_rsv_task.get_rsv_unit(
                keyword='asset-source-maya-scene-src-file'
            )
            i_work_scene_src_file_path = i_work_scene_src_rsv_unit.get_result(
                version='v000'
            )

            _i_option_opt = bsc_core.ArgDictStringOpt(
                option=dict(
                    option_hook_key='rsv-task-batchers/asset/gen-prv-render-submit',
                    file=i_work_scene_src_file_path,
                    #
                    td_enable=True,
                    # test_flag=True,
                )
            )
            #
            ssn_commands.execute_option_hook_by_deadline(
                option=_i_option_opt.to_string()
            )

    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    import lxgui.core as gui_core

    import lxsession.commands as ssn_commands

    rsv_asset = session.rsv_obj

    rsv_project = rsv_asset.get_rsv_project()
    #
    project = rsv_asset.get('project')
    #
    tree_item = rsv_asset.get_obj_gui()
    tree_view = tree_item.get_view()

    all_items = tree_view.get_selected_items()

    assets = []
    for i_item in all_items:
        i_rsv_obj = i_item.get_gui_dcc_obj(namespace='resolver')
        if i_rsv_obj:
            if i_rsv_obj.type_name == 'asset':
                if i_item.get_status() not in [
                    i_item.ValidationStatus.Error, i_item.ValidationStatus.Warning
                ]:
                    assets.append(
                        i_rsv_obj.name
                    )
                else:
                    bsc_log.Log.trace_method_warning(
                        'asset="{}" is not available'.format(i_rsv_obj)
                    )
    #
    if assets:
        gui_core.GuiDialog.create(
            session.gui_name,
            content=(
                'submit selected asset(s) preview render:\n'
                '{}\n'
                'press "Ok" to continue...'
            ).format(
                ',\n'.join(map(lambda x: '"{}"'.format(x), assets))
            ),
            ok_method=ok_method
        )
    else:
        gui_core.GuiDialog.create(
            session.gui_name,
            content='no available asset(s) had be selected',
            status=gui_core.GuiDialog.ValidationStatus.Error
        )


# noinspection PyUnresolvedReferences
main(session)
