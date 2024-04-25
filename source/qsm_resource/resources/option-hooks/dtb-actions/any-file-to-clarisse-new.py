# coding:utf-8


def main(session):
    import lxgeneral.dcc.core as gnl_dcc_core

    option_opt = session.option_opt
    port = option_opt.get_as_integer('port')

    cmd = '''
import lxbasic.resource as bsc_resource
import lxbasic.core as bsc_core
file_path = bsc_resource.ExtendResource.get('scripts/any-file-to-clarisse.py')
bsc_core.ExcExtraMtd.execute_python_file(
    file_path, options=dict(resource_location='{resource_location}', file='{file}')
)
    '''.format(**dict(resource_location=option_opt.get('resource_location'), file=option_opt.get('file')))
    gnl_dcc_core.SocketConnectForClarisse(port).run(cmd)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
