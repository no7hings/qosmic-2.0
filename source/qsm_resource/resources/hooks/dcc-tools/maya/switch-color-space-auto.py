# coding:utf-8


def main(session):
    import lxgeneral.dcc.scripts as gnl_dcc_scripts
    # noinspection PyShadowingNames
    import lxmaya.dcc.objects as mya_dcc_objects
    #
    gnl_dcc_scripts.ScpDccTextures(
        mya_dcc_objects.TextureReferences(
            option=dict(with_reference=True)
        )
    ).auto_switch_color_space()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
