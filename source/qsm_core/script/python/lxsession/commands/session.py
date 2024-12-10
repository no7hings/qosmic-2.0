# coding:utf-8
import six


def set_session_option_hooks_execute_by_deadline(session):
    """
    execute contain option-hooks by deadline
    :param session: <instance of session>
    :return: None
    """
    import lxbasic.log as bsc_log

    import lxbasic.core as bsc_core

    from . import hook as ssn_cmd_hook

    def run_branch_fnc_(batch_option_hook_key_, option_hook_key_, batch_hook_option_, hook_option_override_):
        _batch_hook_option_opt = bsc_core.ArgDictStringOpt(batch_hook_option_)
        _batch_choice_scheme = _batch_hook_option_opt.get('choice_scheme')
        _hook_option_opt = bsc_core.ArgDictStringOpt(
            dict(
                option_hook_key=option_hook_key_,
                #
                batch_file=_batch_hook_option_opt.get('batch_file'),
                # python option
                file=_batch_hook_option_opt.get('file'),
                # application version
                katana_version=_batch_hook_option_opt.get('katana_version'),
                application_version=_batch_hook_option_opt.get('application_version'),
                # standard keys
                user=_batch_hook_option_opt.get('user'),
                host=_batch_hook_option_opt.get('host'),
                time_tag=_batch_hook_option_opt.get('time_tag'),
                #
                choice_scheme=_batch_hook_option_opt.get('choice_scheme'),
                #
                test_flag=_batch_hook_option_opt.get_as_boolean('test_flag'),
                #
                td_enable=_batch_hook_option_opt.get_as_boolean('td_enable'),
                localhost_enable=_batch_hook_option_opt.get_as_boolean('localhost_enable'),
            )
        )
        #
        _hook_option_opt.update_from(
            hook_option_override_
        )
        # add main-key to dependencies
        _dependencies = _hook_option_opt.get('dependencies') or []
        _dependencies.append(batch_option_hook_key_)
        _hook_option_opt.set('dependencies', _dependencies)
        #
        _choice_scheme_includes = _hook_option_opt.get('choice_scheme_includes', as_array=True)
        if _choice_scheme_includes:
            if session._get_choice_scheme_matched_(
                    _batch_choice_scheme,
                    _choice_scheme_includes
            ) is False:
                bsc_log.Log.trace_method_warning(
                    'scheme choice',
                    'option-hook="{}" is ignore'.format(option_hook_key_)
                )
                return
        #
        _inherit_keys = _hook_option_opt.get('inherit_keys', as_array=True)
        if _inherit_keys:
            _hook_option_opt.set('inherit_keys', _inherit_keys)
            for _i_key in _inherit_keys:
                _hook_option_opt.set(
                    _i_key, _batch_hook_option_opt.get(_i_key)
                )
        #
        ssn_cmd_hook.execute_option_hook_by_deadline(
            option=_hook_option_opt.to_string()
        )

    c = session.configure
    option_hook_keys = c.get('option_hooks')
    main_key = session.option_opt.get('option_hook_key')
    with bsc_log.LogProcessContext.create_as_bar(
        maximum=len(option_hook_keys),
        label='option-hooks execute by deadline',
    ) as g_p:
        for i_args in option_hook_keys:
            g_p.do_update()
            if isinstance(i_args, six.string_types):
                i_sub_key = i_args
                run_branch_fnc_(
                    main_key,
                    i_sub_key,
                    session.option,
                    {}
                )
            elif isinstance(i_args, dict):
                for i_k, i_v in i_args.items():
                    i_sub_key = i_k
                    i_script_option = i_v
                    run_branch_fnc_(
                        main_key,
                        i_sub_key,
                        session.option,
                        i_script_option
                    )
