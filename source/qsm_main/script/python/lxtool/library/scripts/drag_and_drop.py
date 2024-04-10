# coding:utf-8
import lxbasic.storage as bsc_storage

import lxbasic.texture as bsc_texture


class ScpTextureResourceData(object):
    def __init__(self, directory_path):
        self._directory_path = directory_path

    def get_texture_path(self):
        directory_opt = bsc_storage.StgDirectoryOpt(self._directory_path)
        texture_paths = directory_opt.get_file_paths(ext_includes=['.tx'])
        if texture_paths:
            return texture_paths[0]
        return None

    def get_texture_assign(self):
        directory_opt = bsc_storage.StgDirectoryOpt(self._directory_path)
        texture_paths = directory_opt.get_file_paths(ext_includes=['.tx'])
        if texture_paths:
            texture_path = texture_paths[0]
            m = bsc_texture.TxrMethodForBuild.generate_instance()
            texture_args = m.generate_all_texture_args(texture_path)
            if texture_args:
                texture_name, texture_data = texture_args
                dict_ = {}
                for k, v in texture_data.items():
                    dict_[k] = v[0]
                return dict_
        return {}


if __name__ == '__main__':
    print ScpTextureResourceData(
        '/production/library/resource/all/surface/mossy_ground_umkkfcolw/v0001/texture/acescg/tx'
    ).get_texture_assign()
