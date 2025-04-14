# coding:utf-8
import urllib

# noinspection PyUnresolvedReferences
from six.moves.urllib.parse import parse_qs, unquote

import socket

from ..wrap import *


class UrlOptions(object):
    @classmethod
    def to_string(cls, options):
        return urllib.urlencode(options)

    @classmethod
    def to_dict(cls, text):
        dict_ = {}
        for k, v in parse_qs(text).items():
            dict_[k] = v[0] if len(v) == 1 else v
        return dict_


class UrlValue(object):
    @classmethod
    def quote(cls, text):
        return urllib.quote_plus(
            ensure_string(text)
        )

    @classmethod
    def unquote(cls, text):
        return unquote(text)


class Socket(object):
    @classmethod
    def is_port_in_use(cls, host, port):
        skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            skt.bind((host, port))
            return False
        except socket.error:
            return True
        finally:
            skt.close()
