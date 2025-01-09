# coding:utf-8
import glob

import os


def _get_file_paths_(directory_paths):
    def _rcs_fnc(path_):
        _results = glob.glob(u'{}/*'.format(path_)) or []
        _results.sort()
        for _path in _results:
            if os.path.isfile(_path):
                lis.append(_path)
            elif os.path.isdir(_path):
                _rcs_fnc(_path)

    lis = []
    [_rcs_fnc(i) for i in directory_paths]
    return lis


if __name__ == '__main__':
    print _get_file_paths_(
        ['/l/prod/cjd/work/assets/cam/cam/rig/cam_rig/maya/']
    )
