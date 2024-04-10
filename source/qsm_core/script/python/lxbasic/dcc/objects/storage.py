# coding:utf-8
import json

import re

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

from .. import abstracts as bsc_dcc_abstracts


class StgDirectory(bsc_dcc_abstracts.AbsStgDirectory):
    def __init__(self, path):
        super(StgDirectory, self).__init__(path)


class StgFile(bsc_dcc_abstracts.AbsStgFile):
    STG_DIRECTORY_CLS = StgDirectory

    def __init__(self, path):
        super(StgFile, self).__init__(path)

    def set_read(self):
        pass

    def set_write(self, raw):
        self.directory.set_create()
        with open(self.path, u'w') as f:
            f.write(raw)
            bsc_log.Log.trace_method_result(
                'file-write',
                u'file="{}"'.format(self.path)
            )

    def set_backup(self):
        backup_file_path = '{}/.backup/{}.{}{}'.format(
            self.directory.path,
            self.name_base,
            self.get_time_tag(),
            self.ext
        )
        self.copy_to_file(backup_file_path)


StgDirectory.STG_FILE_CLS = StgFile


class StgFileForMultiply(bsc_dcc_abstracts.AbsStgFile):
    STG_DIRECTORY_CLS = StgDirectory
    RE_MULTIPLY_PATTERNS = [r'.*?(\$F.*?)[\.]']

    def __init__(self, path):
        super(StgFileForMultiply, self).__init__(path)

    def get_has_elements(self):
        for pattern in self.RE_MULTIPLY_PATTERNS:
            re_pattern = re.compile(pattern, re.IGNORECASE)
            results = re.findall(re_pattern, self.name) or []
            if results:
                return True
        return False

    def set_file_path_convert_to_hou_seq(self):
        file_name = self.name
        pattern = r'[\.].*?(\d+.*?)[\.]'
        results = re.finditer(pattern, file_name, re.IGNORECASE) or []
        if results:
            start, end = list(results)[0].span()
            new_file_name = '{}.$F.{}'.format(file_name[:start], file_name[end:])
            new_file_path = '{}/{}'.format(self.directory.path, new_file_name)
            return new_file_path


class StgJson(bsc_dcc_abstracts.AbsStgFile):
    STG_DIRECTORY_CLS = StgDirectory

    def __init__(self, path):
        super(StgJson, self).__init__(path)

    def set_read(self, encoding=None):
        if self.get_is_exists() is True:
            with open(self.path) as j:
                raw = json.load(j, encoding=encoding)
                j.close()
                return raw

    def set_write(self, raw):
        bsc_storage.StgFileOpt(
            self.get_path()
        ).set_write(raw)


class StgYaml(bsc_dcc_abstracts.AbsStgFile):
    STG_DIRECTORY_CLS = StgDirectory

    def __init__(self, path):
        super(StgYaml, self).__init__(path)

    def set_read(self):
        return bsc_storage.StgFileOpt(
            self.get_path()
        ).set_read()

    def set_write(self, raw):
        bsc_storage.StgFileOpt(
            self.get_path()
        ).set_write(raw)


class StgTexture(bsc_dcc_abstracts.AbsStgTexture):
    STG_DIRECTORY_CLS = StgDirectory
    RE_SEQUENCE_PATTERN = r'.*?(####).*?'

    def __init__(self, path):
        super(StgTexture, self).__init__(path)
