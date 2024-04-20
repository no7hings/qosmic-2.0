# coding:utf-8


def main(session):
    import lxmaya.fnc.objects as mya_fnc_objects

    rsv_entity = session.rsv_obj

    project = rsv_entity.get('project')
    asset = rsv_entity.get('asset')

    mya_fnc_objects.FncBuilderForAssetOld(
        option=dict(
            project=project,
            asset=asset,
            #
            with_model_geometry=True,
            with_groom_geometry=True, with_groom_grow_geometry=True,
            with_surface_look=True, with_surface_geometry_uv_map=True,
            with_camera=True,
            with_light=True,
            save_scene=True,
            render_resolution=(2048, 2048),
        )
    ).set_run()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
