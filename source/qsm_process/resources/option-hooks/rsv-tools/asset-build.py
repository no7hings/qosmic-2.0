# coding:utf-8


def main(session):
    def build_fnc_(project_, asset_):
        import lxmaya.fnc.objects as mya_fnc_objects

        _node = w.get_options_node()
        _option = w.get_options_as_kwargs()

        _render_resolution = _option.pop('render.resolution')

        _option = dict(
            with_model_geometry=_node.get('build_options.with_model_geometry'),
            #
            with_groom_geometry=_node.get('build_options.with_groom_geometry'), with_groom_grow_geometry=_node.get('build_options.with_groom_grow_geometry'),
            #
            with_surface_geometry_uv_map=_node.get('build_options.with_surface_geometry_uv_map'), with_surface_look=_node.get('build_options.with_surface_look'),
            #
            with_camera=_node.get('build_options.with_camera'), with_light=_node.get('build_options.with_light'),
            #
            render_resolution=_node.get('render.resolution'),
            #
            save_scene=_node.get('build_options.save_scene'),
        )
        _option['render_resolution'] = _render_resolution
        _option['project'] = project_
        _option['asset'] = asset_
        #
        mya_fnc_objects.FncBuilderForAssetOld(
            option=_option
        ).set_run()

    def check_all_fnc_():
        for i in node.get_port('build_options').get_children():
            i.set(True)

    def check_clear_fnc_():
        for i in node.get_port('build_options').get_children():
            i.set(False)

    import lxgui.core as gui_core

    import lxresolver.core as rsv_core

    option_opt = session.option_opt

    project = option_opt.get('project')
    asset = option_opt.get('asset')

    r = rsv_core.RsvBase.generate_root()

    content = None
    rsv_entity = r.get_rsv_resource(project=project, asset=asset)
    if rsv_entity:
        w = gui_core.GuiDialog.create(
            session.gui_name,
            content=u'build "{}"\npress "Ok" to continue'.format(asset),
            #
            ok_method=lambda *args, **kwargs: build_fnc_(project, asset),
            #
            options_configure=session.configure.get('build.node.options'),
            window_size=(480, 480),
            use_exec=False,
            use_thread=False,
        )
        node = w.get_options_node()
        node.set('check_all', check_all_fnc_)
        node.set('check_clear', check_clear_fnc_)
    else:
        content = u'"Asset" is non-exists, please call for TD get more help'
    #
    if content is not None:
        gui_core.GuiDialog.create(
            session.gui_name,
            content=content,
            status=gui_core.GuiDialog.ValidationStatus.Error,
            #
            ok_label='Close',
            #
            no_visible=False, cancel_visible=False,
            use_exec=False
        )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
