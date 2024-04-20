# coding:utf-8


def main(session):
    import lxsession.commands as ssn_commands
    #
    rsv_entity = session.rsv_obj

    ssn_commands.set_option_hook_execute(
        'option_hook_key=rsv-tools/asset-camera-create-or-publish&project={project}&asset={asset}'.format(
            **rsv_entity.properties.value
        )
    )


# noinspection PyUnresolvedReferences
main(session)
