# coding:utf-8


def test(option_opt):
    import time

    import lxbasic.log as bsc_log

    print option_opt

    _m = 20

    with bsc_log.LogProcessContext.create_as_bar(maximum=_m, label='test') as l_p:
        for _i in range(_m):
            time.sleep(1)
            l_p.do_update()


def main(session):
    import threading

    import functools
    #
    option_opt = session.get_option_opt()
    key = option_opt.get('method')

    if key in {'test'}:
        t_0 = threading.Thread(
            target=functools.partial(
                test, option_opt
            )
        )
        t_0.start()
        t_0.join()


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
