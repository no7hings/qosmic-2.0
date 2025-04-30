# coding:utf-8
from ..wrap import *

import six

import re

import pypinyin

import itertools


class Text(object):
    @staticmethod
    def split(text):
        return re.split(six.u(r'[^a-zA-Z0-9\u4e00-\u9fff]+'), ensure_unicode(text))

    @staticmethod
    def split_any_to_texts(text):
        return re.findall(six.u(r'[a-zA-Z0-9]+|[\u4e00-\u9fff]+'), ensure_unicode(text))

    # no chines word
    @classmethod
    def split_any_to_words(cls, text):
        list_ = []
        # to string
        text = ensure_unicode(text)

        chars = re.findall(six.u(r'[a-zA-Z0-9]+|[\u4e00-\u9fff]+'), text)
        for i_c in chars:
            # is chinese
            if re.match(six.u(r'[\u4e00-\u9fff]+'), i_c):
                list_.append(''.join(map(lambda x: str(x).capitalize(), pypinyin.lazy_pinyin(i_c))))
            else:
                list_.append(i_c)
        return list_

    @classmethod
    def to_prettify(cls, text):
        return six.u(' ').join(
            map(lambda x: x.capitalize(), cls.split_any_to_texts(text))
        )

    @staticmethod
    def split_any_to_words_extra(text):
        list_ = []
        # to string
        text = ensure_unicode(text)

        chars = re.findall(six.u(r'[a-zA-Z0-9]+|[\u4e00-\u9fff]+'), text)
        for i_c in chars:
            list_.append(i_c)
            # is chinese
            if re.match(six.u(r'[\u4e00-\u9fff]+'), i_c):
                # to pinyin
                list_.append(''.join(map(lambda x: str(x).capitalize(), pypinyin.lazy_pinyin(i_c))))
        return list_

    @staticmethod
    def split_any_to_strings(text):
        list_ = []
        # to string
        text = ensure_unicode(text)

        chars = re.findall(six.u(r'[a-zA-Z0-9]+|[\u4e00-\u9fff]+'), text)
        for i_c in chars:
            # is chinese
            if re.match(six.u(r'[\u4e00-\u9fff]+'), i_c):
                # to pinyin
                list_.append(''.join(map(lambda x: str(x).capitalize(), pypinyin.lazy_pinyin(i_c))))
            else:
                list_.append(i_c)
        return list_

    @classmethod
    def to_dcc_name(cls, text):
        pieces = cls.split_any_to_strings(text)
        name = '_'.join([x.lower() for x in pieces])
        if len(name) > 1:
            if name[0].isdigit():
                return '_'+name
        return name

    @classmethod
    def to_pinyin_name(cls, text):
        list_ = []
        # to string
        text = ensure_unicode(text)

        chars = re.findall(six.u(r'[a-zA-Z0-9]+|[\u4e00-\u9fff]+'), text)
        for i_c in chars:
            # chs
            if re.match(six.u(r'[\u4e00-\u9fff]+'), i_c):
                list_.append('_'.join(map(lambda x: str(x).lower(), pypinyin.lazy_pinyin(i_c))))
            else:
                list_.append(i_c)
        return '_'.join(list_)

    @classmethod
    def to_pinyin_map(cls, text):
        dict_ = {}
        list_ = []
        # to string
        text = ensure_unicode(text)

        chars = re.findall(six.u(r'[a-zA-Z0-9]+|[\u4e00-\u9fff]+'), text)
        for i_c in chars:
            list_.append(i_c)
            # chs
            if re.match(six.u(r'[\u4e00-\u9fff]+'), i_c):
                i_pinyin = ''.join(map(lambda x: str(x).capitalize(), pypinyin.lazy_pinyin(i_c)))
                dict_[i_pinyin] = i_c
        return list_, dict_

    @classmethod
    def find_first_chr(cls, text):
        # to string
        text = ensure_unicode(text)

        chars = re.findall(six.u(r'[a-zA-Z0-9]+|[\u4e00-\u9fff]+'), text)
        if chars:
            c = chars[0]
            if re.match(six.u(r'[\u4e00-\u9fff]+'), c):
                return pypinyin.lazy_pinyin(c)[0][0].lower()
            return c[0].lower()

    @classmethod
    def cleanup(cls, text, stop_on_chs=False):
        list_ = []
        # to string
        text = ensure_unicode(text)

        chars = re.findall(six.u(r'[a-zA-Z0-9]+|[\u4e00-\u9fff]+'), text)
        for i_c in chars:
            # chs
            if re.match(six.u(r'[\u4e00-\u9fff]+'), i_c):
                if stop_on_chs is True:
                    break
            else:
                list_.append(i_c)
        return '_'.join(list_)


class Texts(object):
    @classmethod
    def split_any_to_texts(cls, texts):
        return list(itertools.chain(*map(Text.split_any_to_texts, texts)))

    @classmethod
    def split_any_to_words_extra(cls, texts):
        return list(itertools.chain(*map(Text.split_any_to_words_extra, texts)))


class KeywordFilter(object):
    @classmethod
    def generate_hidden_args(cls, texts_src, texts_tgt):
        # todo: use match all mode then, maybe use match one mode also
        if texts_src and texts_tgt:
            contexts_src = map(ensure_unicode, texts_src)
            context_tgt = '_'.join(cls.to_keys(texts_tgt))
            context_tgt = context_tgt.lower()

            for i_text in contexts_src:
                i_text = i_text.lower()
                if '*' in i_text:
                    i_filter_key = '*{}*'.format(i_text.lstrip('*').rstrip('*'))
                    if not Fnmatch.is_match(context_tgt, i_filter_key):
                        return True, True
                else:
                    if i_text not in context_tgt:
                        return True, True
            return True, False
        return False, False

    @classmethod
    def to_keys(cls, texts):
        if not texts:
            return []

        keys = set()
        # add pinyin to keyword filter
        for i_text in texts:
            if not i_text:
                continue

            i_texts = Text.split_any_to_words_extra(i_text)
            keys.add(i_text)
            keys.update(i_texts)

        return keys
