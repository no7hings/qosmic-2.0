# coding:utf-8
import fnmatch

import re

import parse

import lxresource as bsc_resource


class DdlBase(object):
    CONNECTION = None

    CONTENT = None

    @classmethod
    def _generate_content(cls):
        if cls.CONTENT is not None:
            return cls.CONTENT
        cls.CONTENT = bsc_resource.RscExtendConfigure.get_as_content('deadline/main')
        cls.CONTENT.do_flatten()
        return cls.CONTENT
    
    @classmethod
    def generate_connection(cls):
        if cls.CONNECTION is not None:
            return cls.CONNECTION

        from Deadline import DeadlineConnect

        cct = cls._generate_content()
        c = DeadlineConnect.DeadlineCon(
            cct.get('connection.host'), cct.get('connection.port')
        )
        cls.CONNECTION = c
        return c


class DdlLogPattern(object):
    def __init__(self, pattern):
        self._pattern = pattern
        self._pattern_fnmatch = self.to_fnmatch_pattern(self._pattern)

    @classmethod
    def to_fnmatch_pattern(cls, variant):
        if variant is not None:
            re_pattern = re.compile(r'[{](.*?)[}]', re.S)
            #
            keys = re.findall(re_pattern, variant)
            s = variant
            if keys:
                for key in keys:
                    s = s.replace('{{{}}}'.format(key), '*')
            return s
        return variant

    @property
    def format(self):
        return self._pattern

    @property
    def pattern(self):
        return self._pattern_fnmatch


class AbsDdlLog(object):
    SEP = '\n'

    def __init__(self, raw):
        self._raw = raw
        self._update_lines()

    @classmethod
    def _to_lines(cls, raw, sep):
        return ['{}{}'.format(i, sep) for i in raw.split(sep)]

    @property
    def lines(self):
        return self._lines

    def _update_lines(self):
        self._lines = []
        if self._raw is not None:
            raw = self._raw
            sep = self.SEP
            self._lines = self._to_lines(raw, sep)


class DdlLog(AbsDdlLog):
    SEP = '\n'

    def __init__(self, raw):
        super(DdlLog, self).__init__(raw)

    # noinspection PyUnusedLocal
    def _get_stouts__(self):
        self._memories = []
        self._errors = []
        self._warnings = []
        pattern_0 = DdlLogPattern('{time}: {index}: STDOUT: {content}')
        contents_0 = fnmatch.filter(
            self._lines, pattern_0.pattern
        )
        pattern_0_outs = []
        for i in contents_0:
            p = parse.parse(
                pattern_0.format, i
            )
            if p:
                raw = p['content']
                raw = raw.lstrip().rstrip()
                pattern_0_outs.append(raw)
        #
        pattern_1 = DdlLogPattern('{time} {memory}MB {status} | {content}')
        contents_1 = fnmatch.filter(
            pattern_0_outs, pattern_1.pattern
        )
        pattern_1_outs = []
        for i in contents_1:
            p = parse.parse(
                pattern_1.format, i
            )
            if p:
                memory = int(p['memory'].lstrip().rstrip())
                time = p['time']
                status = p['status'].lstrip().rstrip()
                raw = p['content']
                raw = raw.lstrip().rstrip()
                pattern_1_outs.append(raw)
                if status == 'ERROR':
                    print i
                self._memories.append(memory)
        #
        pattern_2 = DdlLogPattern('[{module}] {content}')
        contents_2 = fnmatch.filter(
            pattern_1_outs, pattern_2.pattern
        )
        for i in contents_2:
            p = parse.parse(
                pattern_2.format, i
            )
            if p:
                print p['module']

    def _get_stouts_(self, content=False):
        lis = []
        pattern_0 = DdlLogPattern('{time}: {index}: STDOUT: {content}')
        lines = fnmatch.filter(
            self._lines, pattern_0.pattern
        )
        for line in lines:
            p = parse.parse(
                pattern_0.format, line
            )
            if p:
                if content is True:
                    lis.append(p['content']+self.SEP)
                else:
                    lis.append(line)
        return lis

    def get_stouts(self, content=False):
        _ = self._get_stouts_(content)
        if _:
            return ''.join(_)

    def _get_infos_(self, content=False):
        lis = []
        pattern_0 = DdlLogPattern('{time}: {index}: INFO: {content}')
        lines = fnmatch.filter(
            self._lines, pattern_0.pattern
        )
        for line in lines:
            p = parse.parse(
                pattern_0.format, line
            )
            if p:
                if content is True:
                    lis.append(p['content']+self.SEP)
                else:
                    lis.append(line)
        return lis

    # noinspection PyUnusedLocal
    def get_infos(self, content=False):
        _ = self._get_infos_()
        if _:
            return ''.join(_)


class DdlLogForArnold(AbsDdlLog):
    SEP = '\n'

    def __init__(self, raw):
        super(DdlLogForArnold, self).__init__(raw)

    def _get_results_(self, status=None, keyword=None, content=False):
        lis = []
        pattern_0 = DdlLogPattern('{time} {memory}MB {status} | {content}')
        lines = fnmatch.filter(
            self._lines, pattern_0.pattern
        )
        for line in lines:
            p = parse.parse(
                pattern_0.format, line
            )
            if p:
                _content = p['content'].lstrip().rstrip()
                _status = p['status'].lstrip().rstrip()
                if status is not None:
                    if _status != status:
                        continue
                #
                if keyword is not None:
                    if keyword not in _content:
                        continue
                #
                if content is True:
                    lis.append(p['content']+self.SEP)
                else:
                    lis.append(line)
        return lis

    def get_errors(self, keyword=None, content=False):
        _ = self._get_results_(status='ERROR', keyword=keyword, content=content)
        if _:
            return ''.join(_)

    def get_warnings(self, keyword=None, content=False):
        _ = self._get_results_(status='WARNING', keyword=keyword, content=content)
        if _:
            return ''.join(_)
