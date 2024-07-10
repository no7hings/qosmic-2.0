# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxsession.commands as ssn_commands

    import lxtool.comparer.gui.widgets as cpr_gui_widgets

    rsv_unit = session.rsv_unit

    session = ssn_commands.get_option_hook_session(
        bsc_core.ArgDictStringOpt(
            dict(
                option_hook_key='rsv-tools/asset-geometry-comparer',
                project=rsv_unit.get('project'),
                asset=rsv_unit.get('asset'),
                step=rsv_unit.get('step'),
                task=rsv_unit.get('task'),
            )
        ).to_string()
    )

    w = cpr_gui_widgets.PnlComparerForAssetGeometry(session)
    w.show_window_auto()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
