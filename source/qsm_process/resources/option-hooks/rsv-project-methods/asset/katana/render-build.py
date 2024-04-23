# coding:utf-8


def main(session):
    import lxkatana.scripts as ktn_scripts

    ktn_scripts.ScpRenderBuild(session).execute()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
