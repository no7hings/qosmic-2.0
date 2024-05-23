# coding:utf-8


def main(session):
    def ok_fnc_():
        pass

    import lxgui.core as gui_core

    dtb_opt = session.get_database_opt()
    if dtb_opt:
        dtb_entity = dtb_opt.get_entity(
            entity_type=session.option_opt.get('entity_type'),
            filters=[
                ('path', 'is', session.option_opt.get('entity'))
            ]
        )
        window = session.get_window()
        w = gui_core.GuiDialog.create(
            label=window.get_window_title(),
            sub_label='{} for {} "{}"'.format(session.gui_name, dtb_entity.entity_type, dtb_entity.gui_name),
            content=(
                u'1. enter a "resource name";\n'
                u'2. press "Confirm" to continue'
            ),
            #
            options_configure=session.configure.get('build.node.options'),
            #
            ok_label='Confirm',
            #
            ok_method=ok_fnc_,
            #
            no_visible=False,
            # show=False,
            #
            window_size=session.gui_configure.get('size'),
            #
            parent=window.widget if window else None,
            #
            use_exec=False,
            #
            use_window_modality=False
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
