# coding:utf-8
import os

import lxbasic.log as bsc_log

from . import base as bsc_cor_base


class UrlMtd(object):
    WINDOWS_BIN_PATHS = [
        "C:/google/Chrome/Application/chrome.exe",
        "D:/google/Chrome/Application/chrome.exe"
    ]
    LINUX_BIN_PATHS = [
        "/opt/google/chrome/google-chrome"
    ]

    @classmethod
    def open_in_chrome(cls, url):
        if bsc_cor_base.SysBaseMtd.get_is_linux():
            bin_paths = cls.LINUX_BIN_PATHS
        elif bsc_cor_base.SysBaseMtd.get_is_windows():
            bin_paths = cls.WINDOWS_BIN_PATHS
        else:
            raise SystemError()
        #
        exists_bin_paths = [i for i in bin_paths if os.path.isfile(i)]
        if exists_bin_paths:
            import webbrowser

            webbrowser.register('Chrome', None, webbrowser.BackgroundBrowser(exists_bin_paths[0]))
            webbrowser.get('Chrome').open(
                url, new=1
            )
        else:
            bsc_log.Log.get_method_error(
                'url method', 'chrome is not found'
            )
