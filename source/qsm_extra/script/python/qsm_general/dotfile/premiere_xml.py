# coding:utf-8
import re

import urllib

from . import abc_


class PremiereXml(abc_.AbsDotXml):
    def __init__(self, *args, **kwargs):
        super(PremiereXml, self).__init__(*args, **kwargs)
        self._root = self._etree.getroot()
        if self._etree.getroot().find('project') is not None:
            self._sequence = self._etree.getroot().find('project').find('children').find('sequence')
        else:
            self._sequence = self._etree.getroot().find('sequence')

    @classmethod
    def _find_one(cls, e_start, key_path):
        key_sequence = key_path.split('.')
        e_cur = e_start
        for i in key_sequence:
            e_next = e_cur.find(i)
            if e_next is None:
                return
            e_cur = e_next
        return e_cur

    @abc_.DotfileCache.get()
    def get_fps(self):
        e = self._find_one(self._sequence, 'rate.timebase')
        return int(float(e.text))

    @abc_.DotfileCache.get()
    def get_videos(self):
        list_ = []
        video_e = self._find_one(self._sequence, 'media.video')
        for i in video_e.findall('track'):
            for j in i.findall('clipitem'):
                j_e = self._find_one(j, 'file.pathurl')
                if j_e is not None:
                    j_text = j_e.text
                    if j_text.startswith('file://localhost/'):
                        j_file_path = urllib.unquote(j_text[len('file://localhost/'):])
                        list_.append(j_file_path)
        return list_

    @abc_.DotfileCache.get()
    def get_files(self):
        print(self._sequence)



