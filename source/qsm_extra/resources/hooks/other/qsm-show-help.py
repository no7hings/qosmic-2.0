# coding:utf-8


def main(session):
    import lxbasic.resource as bsc_resource

    import lxbasic.core as bsc_core

    gui_configure = session.gui_configure

    url_p = gui_configure.get('help_url')
    if url_p:
        cfg = bsc_resource.BscExtendConfigure.get_as_content('dokuwiki/main')
        if bsc_core.BscSystem.get_is_dev():
            host = cfg.get('connection_dev.host')
        else:
            host = cfg.get('connection_new.host')

        url = url_p.format(host=host)

        bsc_core.BscSystem.open_url(url)


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
