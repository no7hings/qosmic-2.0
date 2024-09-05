# coding:utf-8
from .. import core as _core

from . import base as _base


class Profile(object):
    DIRECTORY = 'Y:/deploy/.log/profile'

    @classmethod
    def generate(cls, unique_id=None):
        return cls(
            '{}/process/{}/{}.json'.format(
                cls.DIRECTORY,
                _core.BscSystem.get_date_tag(),
                unique_id or _core.BscUuid.generate_new()
            )
        )

    def __init__(self, file_path):
        self._file_path = file_path

        self._data = dict(
            user=_core.BscSystem.get_user_name(),
            host=_core.BscSystem.get_host(),
            ctime=_core.BscSystem.generate_timestamp()
        )

    @property
    def data(self):
        return self._data

    def update(self, key, value):
        self._data[key] = value
        _base.StgFileOpt(self._file_path).set_write(self._data)

    def update_timestamp(self, key):
        self.update(key, _core.BscSystem.generate_timestamp())

    @classmethod
    def get_data_args(cls, pattern=None):
        status_mapper = _core.BasProcessStatus.to_mapper()
        data_keys = []
        dict_ = {}
        if pattern is not None:
            ptn = pattern
        else:
            ptn = 'Y:/deploy/.log/profile/process/{date}/{uuid}.json'
        ptn_opt = _core.BscStgParseOpt(ptn)
        matches = ptn_opt.get_matches()
        dict_0 = {}
        for i_match in matches:
            i_data = _base.StgFileOpt(i_match['result']).set_read()
            i_date = i_match['date']
            if 'tag' not in i_data:
                continue
            j_method = i_data['tag']
            i_user = i_data['user']
            if 'status' in i_data:
                i_status = i_data['status']
                i_key = '{} | {}'.format(i_user, i_date)
                if i_status == 4:
                    if j_method not in data_keys:
                        data_keys.append(j_method)
                    i_started = i_data['started']
                    i_finished = i_data['finished']
                    i_time = i_finished-i_started
                    dict_0.setdefault(i_key, []).append((j_method, i_time))

        data_keys.sort()
        for k, v in dict_0.items():
            i_dict_0 = {}
            for j in v:
                i_dict_0.setdefault(j[0], []).append(j[1])

            i_dict_1 = {}
            for j_key in data_keys:
                if j_key in i_dict_0:
                    j_times = i_dict_0[j_key]
                    j_time_a = sum(j_times)/len(j_times)
                    i_dict_1[j_key] = j_time_a
                else:
                    i_dict_1[j_key] = 0
            dict_[k] = i_dict_1

        return dict_, data_keys