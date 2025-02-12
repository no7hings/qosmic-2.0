# coding:utf-8
import six as _six


def ensure_string(s):
    if isinstance(s, _six.text_type):
        if _six.PY2:
            return s.encode('utf-8')
    elif isinstance(s, _six.binary_type):
        if _six.PY3:
            return s.decode('utf-8')
    return s


def auto_unicode(text):
    if not isinstance(text, _six.text_type):
        return text.decode('utf-8')
    return text
