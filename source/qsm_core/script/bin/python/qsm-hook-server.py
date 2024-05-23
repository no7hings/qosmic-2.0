# coding:utf-8
from __future__ import print_function

import sys

import getopt

import multiprocessing

from PyQt5 import QtCore, QtWidgets

argv = sys.argv

IS_STARTED = False


def main():
    try:
        opts, args = getopt.getopt(
            argv[1:],
            'ho:',
            ['help', 'option=']
        )
        option = [None] * 1
        for key, value in opts:
            if key in ('-h', '--help'):
                __print_help()
                sys.exit()
            elif key in ('-o', '--option'):
                option = value
        #
        if option is not None:
            __execute_with_option(option)
    #
    except getopt.GetoptError:
        sys.stdout.write('argv error\n')


def __print_help():
    sys.stdout.write(
        '***** qsm-hook-server *****\n'
        '\n'
        '-h or --help: show help\n'
        '-o or --option: set run with option\n'
        'start sever: -o start=true\n'
    )


def __execute_with_option(option):
    import lxbasic.core as bsc_core

    option_opt = bsc_core.ArgDictStringOpt(option)
    # start server
    if option_opt.get_as_boolean('start') or False is True:
        print('abc')
        if IS_STARTED is False:
            __start_server()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("PyQt and Flask")
        self.setGeometry(100, 100, 600, 400)
        self.label = QtWidgets.QLabel("Flask and PyQt Running", self)
        self.label.setGeometry(50, 50, 500, 50)

    def display_error(self, error_message):
        print(error_message)
        # self.label.setText("Error: {error_message}".format(error_message=error_message))


def __start_server():
    def server_quit():
        server_process.terminate()
        server_process.join()

    import qsm_hook.core as qsm_hok_core

    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    server_process = qsm_hok_core.start_server_process()

    # noinspection PyUnresolvedReferences
    app.aboutToQuit.connect(server_quit)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
