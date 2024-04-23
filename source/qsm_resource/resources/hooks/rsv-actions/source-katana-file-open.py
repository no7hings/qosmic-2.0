# coding:utf-8

def main(session):
    import lxresolver.core as rsv_core

    import qsm_prc_general.rsv.operators as utl_rsv_operators

    file_path = session.rsv_unit.get_result(
        version='latest'
    )
    if file_path:
        resolver = rsv_core.RsvBase.generate_root()
        project = session.variants['project']
        rsv_project = resolver.get_rsv_project(project=project)
        if rsv_project is not None:
            rsv_app = rsv_project.get_rsv_app(
                application='katana'
            )
            utl_rsv_operators.RsvKatanaOpt(
                rsv_app
            ).open_file(
                file_path
            )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
