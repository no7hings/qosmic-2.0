# coding:utf-8


def main(session):
    def yes_fnc_():
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
            status=gui_core.GuiDialog.ValidationStatus.Active,
            content=(
                '1. choose a "scheme";\n'
                '    a). default is "custom"\n'
                '2. enter a "resource name";\n'
                '3. press "Confirm" to continue'
            ),
            #
            options_configure=session.configure.get('build.node.options'),
            #
            yes_label='Confirm',
            #
            yes_method=yes_fnc_,
            #
            no_visible=False,
            show=False,
            #
            window_size=session.gui_configure.get('size'),
            #
            parent=window.widget if window else None,
            #
            use_exec=False,
            #
            # use_window_modality=False
        )

        o = w.get_options_node()

        o.set('type', dtb_entity.path)

        w.set_window_show()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
