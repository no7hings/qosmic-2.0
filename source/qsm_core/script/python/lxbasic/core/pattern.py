# coding:utf-8
import glob

import re

import fnmatch

import parse
# scan
from ..scan import glob_ as _scan_glob
# process
from . import base as _base

from . import raw as _raw


class BscPattern:
    @classmethod
    def glob_fnc(cls, p_str):
        _ = glob.glob(
            p_str
        )
        if _:
            if _base.BscSystem.get_is_windows():
                _ = map(lambda x: x.replace('\\', '/'), _)
            return _
        return []


class BscFileTiles:
    RE_UDIM_KEYS = [
        (r'<udim>', r'{}', 4),
    ]
    #
    RE_SEQUENCE_KEYS = [
        # keyword, re_format, count
        (r'#', r'{}', -1),
        # maya
        (r'<f>', r'{}', 4),
        # katana, etc. "test.(0001-0600)%04d.exr"
        (r'(\()[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9](\))(%04d)', r'{}', 4),
        # houdini, etc. "test.$F.exr"
        (r'$F', r'\{}[^\d]', 4),
    ]
    # houdini
    for i in range(4):
        RE_SEQUENCE_KEYS.append(
            (r'$F0{}'.format(i+1), r'\{}', i+1)
        )
    # katana
    for i in range(4):
        RE_SEQUENCE_KEYS.append(
            (r'%0{}d'.format(i+1), r'{}', i+1)
        )
    #
    RE_MULTIPLY_KEYS = RE_UDIM_KEYS+RE_SEQUENCE_KEYS
    PATHSEP = '/'

    @classmethod
    def to_fnmatch_style(cls, pattern):
        re_keys = cls.RE_MULTIPLY_KEYS
        #
        new_name_base = pattern
        for i_k, i_f, i_c in re_keys:
            i_r = re.finditer(i_f.format(i_k), pattern, re.IGNORECASE) or []
            for j in i_r:
                j_start, j_end = j.span()
                if i_c == -1:
                    s = '[0-9]'
                    new_name_base = new_name_base.replace(pattern[j_start:j_end], s, 1)
                else:
                    s = '[0-9]'*i_c
                    new_name_base = new_name_base.replace(pattern[j_start:j_end], s, 1)
        return new_name_base

    @classmethod
    def to_re_style(cls, pattern):
        pattern_ = pattern
        args = BscFileTiles.get_args(pattern)
        for i, (i_key, i_count) in enumerate(args):
            pattern_ = pattern_.replace(
                i_key, r'[PATTERN-PLACEHOLDER-{}]'.format(i), 1
            )
        #
        re_pattern_ = fnmatch.translate(pattern_)
        for i, (i_key, i_count) in enumerate(args):
            re_pattern_ = re_pattern_.replace(
                r'[PATTERN-PLACEHOLDER-{}]'.format(i),
                r'(\d{{{}}})'.format(i_count)
            )
        return re_pattern_

    @classmethod
    def get_args(cls, pattern):
        re_keys = cls.RE_MULTIPLY_KEYS
        #
        key_args = []
        for i_k, i_f, i_c in re_keys:
            results = re.findall(i_f.format(i_k), pattern, re.IGNORECASE) or []
            if results:
                if i_c == -1:
                    i_count = len(results)
                    i_key = i_count*i_k
                else:
                    i_count = i_c
                    i_key = i_k
                #
                key_args.append(
                    (i_key, i_count)
                )
        return key_args

    @classmethod
    def is_valid(cls, p):
        re_keys = cls.RE_MULTIPLY_KEYS
        #
        for i_k, i_f, i_c in re_keys:
            results = re.findall(i_f.format(i_k), p, re.IGNORECASE) or []
            if results:
                return True
        return False


class BscVersion:
    @classmethod
    def to_number_embedded_args(cls, text):
        pieces = re.compile(r'(\d+)').split(text)
        pieces[1::2] = map(int, pieces[1::2])
        return pieces

    @classmethod
    def sort_by_number(cls, texts):
        texts.sort(key=lambda x: cls.to_number_embedded_args(x))
        return texts

    @classmethod
    def get_version_latest(cls, ptn, padding=3):
        ptn_glob = ptn.replace('{version}', '[0-9]'*padding)

        _results = glob.glob(ptn_glob)
        if not _results:
            return None

        _results = cls.sort_by_number(_results)

        result = _results[-1]
        result = result.replace('\\', '/')
        return int(parse.parse(ptn, result)['version'])

    @classmethod
    def generate_as_new_version(cls, ptn, padding=3):
        version_latest = cls.get_version_latest(ptn)
        if version_latest is None:
            version_latest = 1
        else:
            version_latest += 1
        return ptn.format(version=str(int(version_latest)).zfill(padding))

    @classmethod
    def generate_as_latest_version(cls, ptn, padding=3):
        version_latest = cls.get_version_latest(ptn)
        if version_latest is not None:
            return ptn.format(version=str(int(version_latest)).zfill(padding))


class BscVersionOpt(object):
    VERSION_ZFILL_COUNT = 3
    PATTERN = 'v{}'.format('[0-9]'*VERSION_ZFILL_COUNT)

    def __init__(self, text):
        self._validation_(text)
        #
        self._text = text
        self._number = int(text[-self.VERSION_ZFILL_COUNT:])

    def __str__(self):
        return self._text

    def __iadd__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError()
        self._number += int(other)
        self._text = 'v{}'.format(str(self._number).zfill(self.VERSION_ZFILL_COUNT))
        return self

    def __isub__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError()
        if self._number >= other:
            self._number -= int(other)
        else:
            self._number = 0
        self._text = 'v{}'.format(str(self._number).zfill(self.VERSION_ZFILL_COUNT))
        return self

    @classmethod
    def _validation_(cls, text):
        if not fnmatch.filter([text], cls.PATTERN):
            raise TypeError(
                'version: "{}" is Non-match "{}"'.format(text, cls.PATTERN)
            )

    @classmethod
    def is_valid(cls, text):
        return not not fnmatch.filter([text], cls.PATTERN)

    def get_number(self):
        return self._number

    number = property(get_number)

    @classmethod
    def get_default(cls):
        return 'v{}'.format(str(1).zfill(cls.VERSION_ZFILL_COUNT))


class BscParse(object):
    RE_KEY_PATTERN = r'[{](.*?)[}]'

    @classmethod
    def get_keys(cls, p):
        lis_0 = re.findall(re.compile(cls.RE_KEY_PATTERN, re.S), p)
        lis_1 = list(set(lis_0))
        lis_1.sort(key=lis_0.index)
        return lis_1

    @classmethod
    def get_value(cls, key, variants):
        if '.' in key:
            key_ = key.split('.')[0]
            if key_ in variants:
                value_ = variants[key_]
                exec ('{} = \'{}\''.format(key_, value_))
                return eval(key)
        if key in variants:
            return variants[key]

    @classmethod
    def update_variants(cls, p, **kwargs):
        if p is not None:
            keys = cls.get_keys(p)
            variants = kwargs
            # to unicode
            s = _base.ensure_unicode(p)
            if keys:
                for i_k in keys:
                    i_v = cls.get_value(i_k, variants)
                    if i_v is not None and i_v != '*':
                        s = s.replace('{{{}}}'.format(i_k), _base.ensure_unicode(i_v))
            return s
        return p

    @classmethod
    def to_fnmatch_style(cls, p, variants=None):
        if p is not None:
            keys = re.findall(re.compile(cls.RE_KEY_PATTERN, re.S), p)
            s = p
            if keys:
                for i_k in keys:
                    i_v = '*'
                    if isinstance(variants, dict):
                        if i_k in variants:
                            i_v = variants[i_k]
                    s = s.replace('{{{}}}'.format(i_k), i_v)
            return s
        return p


class BscFnmatch(object):
    FILTER_CACHE = dict()
    FILTER_CACHE_MAXIMUM = 1000
    
    MAGIC_CHECK = re.compile('[*?[]')

    @classmethod
    def has_magic(cls, s):
        return cls.MAGIC_CHECK.search(s) is not None

    @classmethod
    def to_re_style(cls, pat):
        i, n = 0, len(pat)
        res = ''
        while i < n:
            c = pat[i]
            i += 1
            if c == '*':
                res += '.*'
            elif c == '?':
                res += '.'
            elif c == '[':
                j = i
                if j < n and pat[j] == '!':
                    j += 1
                if j < n and pat[j] == ']':
                    j += 1
                while j < n and pat[j] != ']':
                    j += 1
                if j >= n:
                    res += '\\['
                else:
                    stuff = pat[i:j].replace('\\', '\\\\')
                    i = j+1
                    if stuff[0] == '!':
                        stuff = '^'+stuff[1:]
                    elif stuff[0] == '^':
                        stuff = '\\'+stuff
                    res = '%s[%s]'%(res, stuff)
            else:
                res = res+re.escape(c)
        return res

    @classmethod
    def is_valid(cls, ptn):
        return ptn != cls.to_re_style(ptn)

    @classmethod
    def filter(cls, texts, p):
        list_ = []
        try:
            re_pat = cls.FILTER_CACHE[p]
        except KeyError:
            res = fnmatch.translate(p)
            if len(cls.FILTER_CACHE) >= cls.FILTER_CACHE_MAXIMUM:
                cls.FILTER_CACHE.clear()
            cls.FILTER_CACHE[p] = re_pat = re.compile(res, re.IGNORECASE)

        match = re_pat.match
        for i_text in texts:
            if match(i_text):
                list_.append(i_text)
        return list_

    @classmethod
    def is_match(cls, text, p):
        try:
            re_pat = cls.FILTER_CACHE[p]
        except KeyError:
            res = fnmatch.translate(p)
            if len(cls.FILTER_CACHE) >= cls.FILTER_CACHE_MAXIMUM:
                cls.FILTER_CACHE.clear()
            cls.FILTER_CACHE[p] = re_pat = re.compile(res, re.IGNORECASE)
        return bool(re_pat.match(text))
    
    @classmethod
    def to_parse_style(cls, p):
        if cls.has_magic(p):
            p_1 = p
            r = re.finditer(r'\*+', p, re.IGNORECASE)
            for i_seq, i in enumerate(r):
                i_start, i_end = i.span()
                p_1 = p_1.replace(p[i_start:i_end], '{{var_{}}}'.format(i_seq), 1)
            return p_1
        return p


class AbsParseOpt(object):

    def __init__(self, p, variants=None):
        p = BscFnmatch.to_parse_style(p)

        self._pattern_origin = p
        self._pattern = p
        
        self._variants = {}
        self._variants_default = variants or {}

        self._pattern_fnmatch_origin = BscParse.to_fnmatch_style(
            self._pattern_origin, self._variants_default
        )
        self._pattern_fnmatch = BscParse.to_fnmatch_style(
            self._pattern, self._variants_default
        )

    def get_pattern(self):
        return self._pattern

    pattern = property(get_pattern)

    def get_pattern_for_fnmatch(self):
        return BscParse.to_fnmatch_style(
            self._pattern, self._variants_default
        )

    pattern_for_fnmatch = property(get_pattern_for_fnmatch)

    def get_keys(self):
        return BscParse.get_keys(
            self._pattern
        )

    keys = property(get_keys)

    def get_value(self):
        return self._pattern

    def update_variants(self, **kwargs):
        keys = self.get_keys()
        for k, v in kwargs.items():
            if k in keys:
                self._variants[k] = v
        #
        self._pattern = BscParse.update_variants(self._pattern, **kwargs)
        self._pattern_fnmatch = BscParse.to_fnmatch_style(
            self._pattern, self._variants_default
        )

    def update_variants_to(self, **kwargs):
        p = self.__class__(self._pattern)
        p.update_variants(**kwargs)
        return p

    def get_variants(self, result, extract=False):
        if _base.BscSystem.get_is_linux():
            i_p = parse.parse(
                self._pattern, result, case_sensitive=True
            )
        elif _base.BscSystem.get_is_windows():
            i_p = parse.parse(
                self._pattern, result, case_sensitive=False
            )
        else:
            raise SystemError()

        if i_p:
            i_r = i_p.named
            if i_r:
                i_r.update(self._variants)
                i_r['result'] = result
                return i_r

        if extract is False:
            return self._variants
        return {}


class BscDccParseOpt(AbsParseOpt):
    def __init__(self, p, variants=None):
        super(BscDccParseOpt, self).__init__(p, variants)


class BscStgParseOpt(AbsParseOpt):
    def __init__(self, p, variants=None):
        super(BscStgParseOpt, self).__init__(p, variants)

    @classmethod
    def to_fnmatch_style_fnc(cls, p, variants=None):
        return BscParse.to_fnmatch_style(p, variants)

    def find_matches(self, sort=False):
        list_ = []

        regex = self.to_fnmatch_style_fnc(
            self._pattern, self._variants_default
        )

        paths = _scan_glob.ScanGlob.glob(
            regex
        )
        if sort is True:
            paths = _raw.RawTextsOpt(paths).sort_by_number()

        # has variant
        if self.get_keys():
            for i_path in paths:
                i_p = parse.parse(
                    self._pattern, i_path, case_sensitive=True
                )
                if i_p:
                    i_r = i_p.named
                    if i_r:
                        i_r.update(self._variants)
                        i_r['result'] = i_path
                        i_r['pattern'] = self._pattern_origin
                        list_.append(i_r)
        else:
            for i_path in paths:
                i_r = dict(result=i_path)
                i_r.update(self._variants)
                list_.append(i_r)
        return list_

    def check_is_matched(self, result):
        return bool(
            fnmatch.filter(
                [result], self._pattern_fnmatch
            )
        )

    def get_exists_results(self, **kwargs):
        p = self.update_variants_to(**kwargs)
        return _scan_glob.ScanGlob.glob(p._pattern_fnmatch)

    def get_match_results(self, sort=False):
        paths = _scan_glob.ScanGlob.glob(
            self.to_fnmatch_style_fnc(
                self._pattern, self._variants_default
            )
        )
        if sort is True:
            paths = _raw.RawTextsOpt(paths).sort_by_number()
        return paths

    def update_default_variants(self, **kwargs):
        self._variants_default.update(kwargs)

    def get_latest_version(self, version_key):
        ms = self.find_matches(sort=True)
        if ms:
            l_m = ms[-1]
            return l_m[version_key]
        return BscVersionOpt.get_default()

    def get_new_version(self, version_key):
        ms = self.find_matches(sort=True)
        if ms:
            l_m = ms[-1]
            l_v = l_m[version_key]
            l_v_p = BscVersionOpt(l_v)
            l_v_p += 1
            return str(l_v_p)
        return BscVersionOpt.get_default()

    def __str__(self):
        return self._pattern


class BscTaskParseOpt(BscStgParseOpt):
    def __init__(self, *args, **kwargs):
        super(BscTaskParseOpt, self).__init__(*args, **kwargs)

    @classmethod
    def to_fnmatch_style_fnc(cls, p, variants=None):
        if 'version' not in variants:
            variants['version'] = '[0-9][0-9][0-9]'
        return BscParse.to_fnmatch_style(p, variants)


class BscDocParseOpt(AbsParseOpt):
    def __init__(self, p, variants=None):
        super(BscDocParseOpt, self).__init__(p, variants)

    def get_matched_lines(self, lines):
        return fnmatch.filter(
            lines,
            self.get_pattern_for_fnmatch()
        )
