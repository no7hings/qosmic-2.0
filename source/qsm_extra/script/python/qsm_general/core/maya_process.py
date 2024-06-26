# coding:utf-8
import lxbasic.storage as bsc_storage

import lxbasic.core as bsc_core


class MayaCacheProcess(object):
    @classmethod
    def generate_command(cls, option):
        if bsc_core.BasApplication.get_is_maya():
            maya_version = bsc_core.BasApplication.get_maya_version()
        else:
            maya_version = '2019'
        # do not use unicode
        # windows
        cmd_scripts = [
            'rez-env maya-{} mtoa qsm_dcc_main'.format(maya_version),
            (
                r'-- mayabatch -command '
                r'"python('
                r'\"import lxsession.commands as ssn_commands;'
                r'ssn_commands.execute_option_hook(option=\\\"{hook_option}\\\")\")"'
            ).format(
                hook_option='option_hook_key=dcc-process/maya-cache-process&' + option
            )
        ]
        return ' '.join(cmd_scripts)

    @classmethod
    def to_option(cls, method, option_dict):
        key = bsc_core.BscHash.to_hash_key(option_dict)
        file_path = cls.to_option_file_path(key)
        bsc_storage.StgFileOpt(file_path).set_write(option_dict)
        return 'method={}&method_option={}'.format(method, key)

    @classmethod
    def to_option_file_path(cls, key):
        root = bsc_core.EnvBaseMtd.get_cache_temporary_root()
        user_name = bsc_core.BscSystem.get_user_name()
        region = bsc_storage.StgTmpBaseMtd.get_save_region(key)
        return '{}/.method-option/{}/{}/{}.json'.format(
            root, user_name, region, key
        )

    @classmethod
    def to_option_dict(cls, option):
        option_opt = bsc_core.ArgDictStringOpt(option)
        key = option_opt.get('method_option')
        file_path = cls.to_option_file_path(key)
        return bsc_storage.StgFileOpt(file_path).set_read()

    @classmethod
    def generate_cmd_script_by_option_dict(cls, method, option_dict):
        option = cls.to_option(method, option_dict)
        return cls.generate_command(option)
