# coding:utf-8
import fnmatch
import os.path

import scandir


class ScanGlob(object):
    @classmethod
    def san_next(cls, path):
        list_ = []
        if os.path.isdir(path):
            for i in scandir.scandir(path):
                if i.is_dir():
                    list_.append(i.path.replace('\\', '/'))
        return list_

    @classmethod
    def glob(cls, regex):
        def _rcs_fnc(path_, depth_, is_root=False):
            _depth = depth_+1
            if _depth <= depth_maximum:
                _filter_name = filter_names[_depth]
                if is_root is True:
                    _filter_path = '*/*'
                else:
                    _filter_path = '{}/{}'.format(
                        path_, _filter_name
                    )
                _child_paths = cls.san_next(path_)
                _filter_child_paths = fnmatch.filter(
                    _child_paths, _filter_path
                )
                if _filter_child_paths:
                    for _i_filter_child_path in _filter_child_paths:
                        if _depth == depth_maximum:
                            list_.append(_i_filter_child_path)
                        _rcs_fnc(_i_filter_child_path, _depth)

        #
        list_ = []
        #
        filter_names = regex.split('/')
        depth_maximum = len(filter_names)-1

        root = filter_names[0]+'/'
        _rcs_fnc(root, 0, is_root=True)
        return list_


if __name__ == '__main__':
    print ScanGlob.glob('X:/QSM_TST/Assets/*/*/Rig/Final')
