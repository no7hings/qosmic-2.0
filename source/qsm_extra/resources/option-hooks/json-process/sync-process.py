# coding:utf-8
import sys


def main(session):
    import lxbasic.storage as bsc_storage

    json_path = session.option_opt.get('json')

    data = bsc_storage.StgFileOpt(json_path).set_read()

    print data


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
