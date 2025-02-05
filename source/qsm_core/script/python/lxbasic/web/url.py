# coding:utf-8
import six

import urllib

if six.PY2:
    # python 2
    # noinspection PyCompatibility
    from urlparse import parse_qs, unquote
else:
    # python 3
    # noinspection PyUnresolvedReferences,PyCompatibility
    from urllib.parse import parse_qs, unquote

import socket


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
    @staticmethod
    def auto_unicode(path):
        if not isinstance(path, six.text_type):
            return path.decode('utf-8')
        return path

    @staticmethod
    def ensure_unicode(s):
        if isinstance(s, six.text_type):
            return s
        elif isinstance(s, bytes):
            return s.decode('utf-8')
        else:
            return s

    @staticmethod
    def ensure_string(path):
        if isinstance(path, six.text_type):
            return path.encode('utf-8')
        return path

    @classmethod
    def quote(cls, text):
        return urllib.quote_plus(
            cls.ensure_string(text)
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
