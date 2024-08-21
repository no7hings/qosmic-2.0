# coding:utf-8


def main(session):
    import lxkatana.core as ktn_core

    import lxbasic.database as bsc_database

    import lxtool.library.scripts as lib_scripts

    import lxkatana.scripts as ktn_scripts

    dtb_opt = session.get_database_opt()
    if dtb_opt:
        window = session.find_window()
        #
        dtb_resource = dtb_opt.get_entity(
            entity_type=session.option_opt.get('entity_type'),
            filters=[
                ('path', 'is', session.option_opt.get('entity'))
            ]
        )

        dtb_resource_opt = bsc_database.DtbNodeOpt(dtb_opt, dtb_resource)
        dtb_version = dtb_resource_opt.get_as_node('version')
        #
        storage_dtb_path = '{}/{}'.format(dtb_version.path, 'texture_acescg_tx_directory')
        dtb_storage = dtb_opt.get_entity(
            entity_type=dtb_opt.EntityTypes.Storage,
            filters=[
                ('path', 'is', storage_dtb_path)
            ]
        )
        dtb_storage_opt = bsc_database.DtbNodeOpt(dtb_opt, dtb_storage)
        directory_stg_path = dtb_storage_opt.get('location')
        texture_assign = lib_scripts.ScpTextureResourceData(directory_stg_path).get_texture_assign()
        if not texture_assign:
            return

        tab_opt = ktn_core.GuiNodeGraphTabOpt()
        ktn_group = tab_opt.get_current_group()
        if not ktn_group:
            return

        obj_opt = ktn_core.NGNodeOpt(ktn_group)
        texture_name = '_'.join(dtb_resource.gui_name.split(' ')).lower()
        ktn_scripts.ScpTextureBuildForDrop(
            obj_opt,
            texture_name,
            texture_assign,
        ).accept()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
