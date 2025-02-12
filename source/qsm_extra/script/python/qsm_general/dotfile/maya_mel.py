# coding:utf-8
from __future__ import print_function

import re

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.translate as bsc_translate

from . import abc_


class MayaMelPreset(abc_.AbsDotfile):
    LOCATION = 'C:/Program Files/Autodesk/Maya2020/presets/attrPresets'

    def __init__(self, *args, **kwargs):
        super(MayaMelPreset, self).__init__(*args, **kwargs)

    @classmethod
    def generate_from_preset_mel(cls, mel_path):
        print(mel_path)

    def to_dict(self):
        dict_ = {}
        p_0 = r'blendAttr "(.*)" (.*);'+self.SEP

        for i_line in self._lines:
            i_r_0 = re.search(p_0, i_line)
            if i_r_0:
                i_key = i_r_0.group(1)
                i_value = i_r_0.group(2)
                dict_[i_key] = eval(i_value)
        return dict_

    @classmethod
    def generate_template_for(cls, node_type):
        dict_ = {}
        directory_path = '{}/{}'.format(cls.LOCATION, node_type)
        file_paths = bsc_storage.StgDirectoryOpt(directory_path).get_file_paths(ext_includes=['.mel'])

        with bsc_log.LogProcessContext.create(maximum=len(file_paths), label='generate template') as l_p:
            for i_file_path in file_paths:
                i_key = bsc_storage.StgFileOpt(i_file_path).name_base
                i_name = bsc_core.BscCamelcaseStr.to_prettify(i_key)
                i_name_chs = bsc_translate.GoogleTranslate.eng_to_chs(i_name)

                i_data = dict(
                    name=i_name,
                    name_chs=i_name_chs,
                    properties=cls(i_file_path).to_dict()
                )

                dict_[i_key] = i_data

                l_p.do_update()

        return dict_


