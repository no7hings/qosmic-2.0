# coding:utf-8


def main(session):
    import lxbasic.core as bsc_core

    import lxbasic.storage as bsc_storage

    dtb_opt = session.get_database_opt()
    if dtb_opt:
        dtb_entity = dtb_opt.get_entity(
            entity_type=session.option_opt.get('entity_type'),
            filters=[
                ('path', 'is', session.option_opt.get('entity'))
            ]
        )
        dtb_port = dtb_opt.get_entity(
            entity_type=dtb_opt.EntityTypes.Attribute,
            filters=[
                ('node', 'is', dtb_entity.path),
                ('port', 'is', 'location'),
            ],
            new_connection=False
        )
        #
        bsc_storage.StgPathOpt(
            dtb_port.value
        ).open_in_system()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
