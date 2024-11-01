# coding:utf-8
from .. import core as _core

from . import base as _base


class Statistics(object):
    DIRECTORY = 'Y:/deploy/.log/statistics'

    @classmethod
    def generate(cls):
        return cls(
            '{}/process/{}/{}.json'.format(
                cls.DIRECTORY, _core.BscSystem.get_date_tag(), _core.BscSystem.get_user_name()
            )
        )

    def __init__(self, file_path):
        self._file_path = file_path
        if _base.StgPath.get_is_file(self._file_path):
            self._data = _base.StgFileOpt(self._file_path).set_read()
        else:
            self._data = dict()

    def update(self, key, value):
        self._data[key] = value
        # noinspection PyBroadException
        try:
            _base.StgFileOpt(self._file_path).set_write(self._data)
        except Exception:
            pass

    def update_at_time(self, value):
        self.update(str(_core.BscSystem.get_time_tag()), value)

    @classmethod
    def get_data_args(cls, pattern=None):
        data_keys = []
        dict_ = {}
        if pattern is not None:
            ptn = pattern
        else:
            ptn = 'Y:/deploy/.log/statistics/process/{date}/{user}.json'
        ptn_opt = _core.BscStgParseOpt(ptn)
        matches = ptn_opt.find_matches()
        dict_0 = {}
        for i_match in matches:
            i_data = _base.StgFileOpt(i_match['result']).set_read()
            i_user = i_match['user']
            i_date = i_match['date']
            i_key = '{} | {}'.format(i_user, i_date)
            for j_k, j_v in i_data.items():
                j_method = j_v['method']
                if j_method not in data_keys:
                    data_keys.append(j_method)
                dict_0.setdefault(i_key, []).append((j_method, j_k))

        data_keys.sort()
        for k, v in dict_0.items():
            i_dict_0 = {}
            for j in v:
                i_dict_0.setdefault(j[0], []).append(j[1])

            i_dict_1 = {}
            for j_key in data_keys:
                if j_key in i_dict_0:
                    i_dict_1[j_key] = len(i_dict_0[j_key])
                else:
                    i_dict_1[j_key] = 0
            dict_[k] = i_dict_1
        return dict_, data_keys
