# coding:utf-8
import collections

import parse

import lxresource as bsc_resource

import lxbasic.storage as bsc_storage


class RsvConfigure(object):
    MainKeys = [
        'builtin',
        'variant',
        'main',
        'framework',
        'project',
        'storage',
        'dcc'
    ]
    MainSchemes = [
        'default',
        'new'
    ]

    @classmethod
    def get_raw(cls, scheme):
        raw = collections.OrderedDict()
        for i_key in cls.MainKeys:
            i_file = bsc_resource.RscExtendConfigure.get_yaml('resolver/{}/{}'.format(scheme, i_key))
            if i_file is not None:
                i_raw = bsc_storage.StgFileOpt(i_file).set_read() or {}
                raw.update(i_raw)
        return raw

    @classmethod
    def get_basic_raw(cls):
        return cls.get_raw('basic')

    @classmethod
    def get_all_default_raws(cls):
        list_ = []
        for i_scheme in cls.MainSchemes:
            i_raw = cls.get_raw(i_scheme)
            list_.append(i_raw)
        return list_


class RsvBase(object):

    URL_PATTERN = 'url://resolver?{parameters}'

    RSV_ROOT = None

    @classmethod
    def parse_url(cls, url):
        dic = {}
        p = parse.parse(
            cls.URL_PATTERN, url, case_sensitive=True
        )
        if p:
            parameters = p['parameters']
            results = parameters.split('&')
            for result in results:
                if result:
                    key, value = result.split('=')
                    dic[key] = value
            if 'file' in dic:
                k = dic['file']
                keyword = '{}-file'.format(k)
                dic['keyword'] = keyword
        else:
            raise TypeError('url: "{}" is not available')
        return dic

    @classmethod
    def generate_root(cls):
        if cls.RSV_ROOT is not None:
            return cls.RSV_ROOT

        from .. import objects as rsv_objects

        rsv_root = rsv_objects.RsvRoot()
        cls.RSV_ROOT = rsv_root
        return cls.RSV_ROOT
