# coding:utf-8
import lxbasic.core as bsc_core

from .. import core as rsv_core


class ScpEnvironment(object):
    """
import lxresolver.scripts as rsv_scripts
print rsv_scripts.ScpEnvironment.get_data('/production/shows/nsa_dev/assets/chr/td_test/user/work.dongchangbao/katana/scenes/surface/td_test.srf.surface.v000_002.katana')
    """

    @classmethod
    def register_from_scene(cls, file_path):
        resolver = rsv_core.RsvBase.generate_root()
        keys = resolver.VariantTypes.Constructs
        #
        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(
            file_path
        )
        if rsv_scene_properties:
            dict_ = rsv_scene_properties.get_value()
        else:
            dict_ = {}
        #
        for i_key in keys:
            i_env_key = 'PG_{}'.format(i_key.upper())
            #
            if i_key in dict_:
                i_env_value = dict_[i_key]
            else:
                i_env_value = ''
            #
            bsc_core.EnvBaseMtd.set(
                i_env_key, i_env_value
            )

    @classmethod
    def get_data(cls, file_path):
        if file_path:
            resolver = rsv_core.RsvBase.generate_root()
            keys = resolver.VariantTypes.Constructs
            #
            rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(
                file_path
            )
            if rsv_scene_properties:
                data = []
                #
                dict_ = rsv_scene_properties.get_value()
                #
                for i_key in keys:
                    i_env_key = 'PG_{}'.format(i_key.upper())
                    #
                    if i_key in dict_:
                        i_env_value = dict_[i_key]
                    else:
                        i_env_value = ''
                    #
                    data.append(
                        (i_key, i_env_key, i_env_value)
                    )
                return True, data
        return False, None

    @classmethod
    def get_as_dict(cls):
        dict_ = {}
        resolver = rsv_core.RsvBase.generate_root()
        keys = resolver.VariantTypes.Constructs
        for i_key in keys:
            i_env_key = 'PG_{}'.format(i_key.upper())
            i_env_value = bsc_core.EnvBaseMtd.get(i_env_key)
            if i_env_value:
                dict_[i_key] = i_env_value
        return dict_
