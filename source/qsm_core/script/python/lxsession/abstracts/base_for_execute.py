# coding:utf-8
import locale

import lxbasic.content as bsc_content

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.extra.methods as bsc_etr_methods


class AbsHookExecutor(object):
    SHELL_PATTERN = '-- qsm-hook-engine -o "{option}"'
    DEADLINE_PATTERN = '-- qsm-hook-engine -o "{option}&start_index=<STARTFRAME>&end_index=<ENDFRAME>"'
    #
    SUBMITTER_CLS = None

    def __init__(self, session):
        self._session = session

    def get_session(self):
        return self._session

    session = property(get_session)

    def execute_with_deadline(self):
        session = self.get_session()

        name = session.get_type()
        return self._submit_deadline_job_(
            session, name, dict(platform=bsc_core.BscSystem.get_platform())
        )

    def _submit_deadline_job_(self, session, name, option_extra_variants, deadline_configure=None):
        hook_option_opt = session.get_option_opt()
        hook_option = session.get_option()
        submit_key = hook_option_opt.get('option_hook_key')
        #
        ssn_ddl_configure = session.get_ddl_configure()
        #
        self._ddl_submiter = self.SUBMITTER_CLS()
        self._ddl_submiter.set_option(
            batch_name=session.get_batch_name(),
            type=session.get_type(),
            name=name,
            group=session.get_group(),
            engine=session.get_engine(),
            hook=session.get_name(),
            #
            user=hook_option_opt.get('user'),
            time_tag=hook_option_opt.get('time_tag'),
        )
        # update task properties
        self._ddl_submiter.set_option_extra(
            **option_extra_variants
        )
        # load deadline options from session configure
        self._ddl_submiter.option.set('deadline.group', ssn_ddl_configure.get('group'))
        self._ddl_submiter.option.set('deadline.pool', ssn_ddl_configure.get('pool'))
        # job software
        deadline_job_software = ssn_ddl_configure.get('job_software')
        if deadline_job_software:
            self._ddl_submiter.job_plug.set(
                'Software', deadline_job_software
            )
        # load deadline options from deadline configure
        if deadline_configure is not None:
            # "job_context" default is not discard
            deadline_job_context = ssn_ddl_configure.get('job_context')
            if deadline_job_context:
                content_0 = deadline_configure.get_as_content(deadline_job_context)
                step = option_extra_variants.get('step')
                if step:
                    content_1 = content_0.get_as_content(step)

                else:
                    content_1 = content_0.get_as_content('default')
                #
                if content_1:
                    self._ddl_submiter.option.set('deadline.priority', content_1.get('priority'))
                    self._ddl_submiter.option.set('deadline.group', content_1.get('group'))
                    self._ddl_submiter.option.set('deadline.pool', content_1.get('pool'))
                    self._ddl_submiter.option.set('deadline.secondary_pool', content_1.get('secondary_pool'))
                    self._ddl_submiter.option.set('deadline.machine_limit', content_1.get('machine_limit'))
        #
        error_limit = ssn_ddl_configure.get('error_limit')
        if error_limit is not None:
            self._ddl_submiter.job_info.set(
                'FailureDetectionTaskErrors', error_limit
            )
        #
        batch_key = hook_option_opt.get('batch_key')
        if batch_key:
            batch_list = hook_option_opt.get(batch_key, as_array=True) or []
            self._ddl_submiter.job_info.set(
                'Frames', ','.join(map(str, range(len(batch_list))))
            )
        # check is render mode
        renderer = hook_option_opt.get('renderer')
        render_node = hook_option_opt.get('render_node')
        if renderer or render_node:
            render_output_directory_path = hook_option_opt.get('render_output_directory')
            if render_output_directory_path:
                self._ddl_submiter.option.set('deadline.output_directory', render_output_directory_path)
            #
            render_frames = hook_option_opt.get('render_frames', as_array=True)
            if render_frames:
                self._ddl_submiter.job_info.set(
                    'Frames', ','.join(render_frames)
                )
        else:
            file_path = hook_option_opt.get('file')
            if file_path:
                self._ddl_submiter.option.set('deadline.output_file', file_path)
        # priority
        deadline_priority = hook_option_opt.get('deadline_priority')
        if deadline_priority is not None:
            self._ddl_submiter.job_info.set('Priority', int(deadline_priority))
        #
        option_hook_key_over = hook_option_opt.get('option_hook_key_over', as_array=True)
        if option_hook_key_over:
            keys = option_hook_key_over
            submit_key = '/'.join(keys)
            self._ddl_submiter.option.set('hook', submit_key)
        else:
            option_hook_key_extend = hook_option_opt.get('option_hook_key_extend', as_array=True)
            if option_hook_key_extend:
                keys = [submit_key]
                keys.extend(option_hook_key_extend)
                submit_key = '/'.join(keys)
                self._ddl_submiter.option.set('hook', submit_key)
        #
        self._ddl_submiter.job_info.set(
            'Comment', hook_option
        )
        ddl_command = self.get_deadline_command()
        if bsc_core.RawTextOpt(ddl_command).get_is_contain_chinese():
            ddl_command = ddl_command.encode(locale.getdefaultlocale()[1])
        #
        self._ddl_submiter.option.set(
            'deadline.command',
            ddl_command
        )
        #
        hook_dependent_ddl_job_ids = session.find_dependent_ddl_job_ids(hook_option)
        if isinstance(hook_dependent_ddl_job_ids, (tuple, list)):
            self._ddl_submiter.job_info.set('JobDependencies', ','.join(hook_dependent_ddl_job_ids))
            self._ddl_submiter.job_info.set('ResumeOnCompleteDependencies', True)
        #
        dependent_ddl_job_id_extend = hook_option_opt.get('dependent_ddl_job_id_extend', as_array=True)
        if dependent_ddl_job_id_extend:
            dependent_ddl_job_ids_string_old = self._ddl_submiter.job_info.get('JobDependencies')
            dependent_ddl_job_id_extend_string = ','.join(dependent_ddl_job_id_extend)
            if dependent_ddl_job_ids_string_old:
                self._ddl_submiter.job_info.set(
                    'JobDependencies',
                    ','.join([dependent_ddl_job_ids_string_old, dependent_ddl_job_id_extend_string])
                )
                self._ddl_submiter.job_info.set(
                    'ResumeOnCompleteDependencies',
                    True
                )
            else:
                dependent_ddl_job_ids_string_new = '{},{}'.format(
                    dependent_ddl_job_ids_string_old, dependent_ddl_job_id_extend_string
                )
                self._ddl_submiter.job_info.set('JobDependencies', dependent_ddl_job_ids_string_new)
                self._ddl_submiter.job_info.set('ResumeOnCompleteDependencies', True)
        # when "td_enable" is discard, override deadline pool and group options
        td_enable = hook_option_opt.get('td_enable') or False
        if td_enable is True:
            self._ddl_submiter.job_info.set(
                'Pool', 'td'
            )
            self._ddl_submiter.job_info.set(
                'SecondaryPool', 'td'
            )
            self._ddl_submiter.job_info.set(
                'Group', 'td'
            )
            self._ddl_submiter.job_info.set(
                'Whitelist', bsc_core.BscSystem.get_host()
            )
        # when "localhost" is discard, override deadline pool and group options
        localhost_enable = hook_option_opt.get('localhost_enable') or False
        if localhost_enable is True:
            self._ddl_submiter.job_info.set(
                'Pool', 'artist'
            )
            self._ddl_submiter.job_info.set(
                'SecondaryPool', 'artist'
            )
            self._ddl_submiter.job_info.set(
                'Group', 'artist'
            )
            self._ddl_submiter.job_info.set(
                'Whitelist', bsc_core.BscSystem.get_host()
            )
        #
        exists_ddl_job_id = session.find_ddl_job_id(hook_option)
        if exists_ddl_job_id:
            session._ddl_job_id = exists_ddl_job_id
            bsc_log.Log.trace_method_warning(
                'option-hook execute by deadline', 'option-hook="{}", job-id="{}" is exists'.format(
                    submit_key, exists_ddl_job_id
                )
            )
        else:
            ddl_job_id = self._ddl_submiter.set_job_submit()
            if ddl_job_id is not None:
                session._ddl_job_id = ddl_job_id
                #
                session.update_ddl_result(
                    hook_option, ddl_job_id
                )
                bsc_log.Log.trace_method_result(
                    'option-hook execute by deadline', 'option-hook="{}", job-id="{}"'.format(
                        submit_key, ddl_job_id
                    )
                )
        return self._ddl_submiter.get_job_result()

    def execute_with_shell(self, block=False):
        #
        environs_extend = {}
        #
        _ = bsc_core.EnvBaseMtd.get('QSM_EXTEND_RESOURCES')
        if _:
            environs_extend['QSM_EXTEND_RESOURCES'] = _
        #
        cmd = self.get_shell_command()
        #
        if block is True:
            bsc_core.PrcBaseMtd.execute_with_result(
                cmd, environs_extend=environs_extend
            )
        else:
            bsc_core.PrcBaseMtd.set_run_with_result_use_thread(
                cmd, environs_extend=environs_extend
            )

    def set_run(self):
        return self.execute_with_deadline()

    def get_shell_command(self):
        etr_utility = bsc_etr_methods.EtrBase
        # todo: use release packages?
        command = etr_utility.get_base_command(
            args_execute=[
                self.SHELL_PATTERN.format(
                    **dict(option=self.get_session().get_option())
                )
            ],
            packages_extend=etr_utility.get_base_packages_extend()
        )
        return command

    def get_deadline_command(self):
        etr_utility = bsc_etr_methods.EtrBase
        # todo: use release packages?
        command = etr_utility.get_base_command(
            args_execute=[
                self.DEADLINE_PATTERN.format(
                    **dict(option=self.get_session().get_option())
                ).replace(
                    '<', '\\<'
                ).replace(
                    '>', '\\>'
                )
            ],
            packages_extend=etr_utility.get_base_packages_extend()
        )
        return command


# project job
class AbsRsvProjectMethodHookExecutor(AbsHookExecutor):
    def __init__(self, *args, **kwargs):
        super(AbsRsvProjectMethodHookExecutor, self).__init__(*args, **kwargs)

    def execute_with_deadline(self):
        session = self.get_session()
        rsv_properties = session.get_rsv_properties()
        if rsv_properties:
            rsv_project = session.get_rsv_project()
            deadline_configure = None
            deadline_configure_file_path = bsc_etr_methods.EtrBase.get_deadline_configure_file(
                rsv_project
            )
            if deadline_configure_file_path:
                if bsc_storage.StgPathMtd.get_is_exists(deadline_configure_file_path):
                    deadline_configure = bsc_content.Content(value=deadline_configure_file_path)
            job_name = session.get_ddl_job_name()
            return self._submit_deadline_job_(
                session, job_name, rsv_properties.value, deadline_configure
            )

    def set_run(self):
        return self.execute_with_deadline()


# task job
class AbsRsvTaskMethodHookExecutor(AbsHookExecutor):
    def __init__(self, *args, **kwargs):
        super(AbsRsvTaskMethodHookExecutor, self).__init__(*args, **kwargs)

    def execute_with_deadline(self):
        import lxresolver.core as rsv_core

        session = self.get_session()
        resolver = rsv_core.RsvBase.generate_root()

        hook_option_opt = session.get_option_opt()

        scene_file_path = hook_option_opt.get('file')

        rsv_scene_properties = resolver.get_rsv_scene_properties_by_any_scene_file_path(
            file_path=scene_file_path
        )
        if rsv_scene_properties:
            rsv_project = session.get_rsv_project()
            deadline_configure = None
            deadline_configure_file_path = bsc_etr_methods.EtrBase.get_deadline_configure_file(
                rsv_project
            )
            if deadline_configure_file_path:
                if bsc_storage.StgPathMtd.get_is_exists(deadline_configure_file_path):
                    deadline_configure = bsc_content.Content(value=deadline_configure_file_path)
            #
            job_name = session._get_rsv_task_version_(rsv_scene_properties)
            return self._submit_deadline_job_(
                session, job_name, rsv_scene_properties.value, deadline_configure
            )

    def set_run(self):
        return self.execute_with_deadline()
