# coding:utf-8
import urllib

import urlparse


class UrlOptions(object):
    @classmethod
    def to_string(cls, options):
        return urllib.urlencode(options)

    @classmethod
    def to_dict(cls, text):
        dict_ = {}
        for k, v in urlparse.parse_qs(text).iteritems():
            dict_[k] = v[0] if len(v) == 1 else v
        return dict_
