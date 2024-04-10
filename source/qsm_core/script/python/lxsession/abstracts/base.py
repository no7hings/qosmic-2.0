# coding:utf-8
import lxcontent.core as ctt_core

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.session as bsc_session

import lxbasic.database as bsc_database
# session
from .. import core as ssn_core


class AbsSsnGenerForResolver(bsc_session.AbsSsnGener):
    def __init__(self, *args, **kwargs):
        self._rsv_obj = args[0]
        self._rsv_properties = self._rsv_obj.properties
        #
        kwargs['variants'] = self._rsv_properties.value
        super(AbsSsnGenerForResolver, self).__init__(
            *args, **kwargs
        )

    def get_rsv_obj(self):
        return self._rsv_obj

    rsv_obj = property(get_rsv_obj)

    def get_rsv_properties(self):
        return self._rsv_properties

    rsv_properties = property(get_rsv_properties)

    def get_obj_gui(self):
        return self._rsv_obj.get_gui_attribute('gui_obj')


class AbsSsnShotgunBaseDef(object):
    def _init_shotgun_base_def_(self):
        pass

    def get_shotgun_connector(self):
        import lxbasic.shotgun as bsc_shotgun

        return bsc_shotgun.StgConnector()

    shotgun_connector = property(get_shotgun_connector)


class AbsSsnRsvUnitDef(object):
    def _set_rsv_unit_def_init_(self, rsv_obj, configure):
        self._rsv_keyword = configure.get('resolver.rsv_unit.keyword')
        #
        self._rsv_unit_version = configure.get('resolver.rsv_unit.version')
        self._rsv_unit_extend_variants = configure.get('resolver.rsv_unit.variants_extend') or {}
        self._rsv_unit = None
        if self._rsv_keyword:
            variants = configure.get('variants')
            self._rsv_keyword = self._rsv_keyword.format(**variants)
            self._rsv_unit = rsv_obj.get_rsv_unit(
                keyword=self._rsv_keyword
            )
            self._rsv_unit_extend_variants['artist'] = bsc_core.SysBaseMtd.get_user_name()

    @property
    def rsv_task(self):
        return self._rsv_unit.get_rsv_task()

    @property
    def rsv_step(self):
        return self._rsv_unit.get_rsv_setp()

    @property
    def rsv_entity(self):
        return self._rsv_unit.get_rsv_resource()

    @property
    def rsv_unit(self):
        return self._rsv_unit

    @property
    def rsv_keyword(self):
        return self._rsv_keyword

    @property
    def rsv_unit_version(self):
        return self._rsv_unit_version

    @property
    def rsv_unit_extend_variants(self):
        return self._rsv_unit_extend_variants

    def set_view_gui(self, prx_widget):
        self._view_gui = prx_widget

    def get_view_gui(self):
        return self._view_gui


class AbsSsnRsvAction(
    AbsSsnGenerForResolver,
    AbsSsnShotgunBaseDef
):
    def __init__(self, *args, **kwargs):
        super(AbsSsnRsvAction, self).__init__(*args, **kwargs)
        if self.get_is_loadable():
            self._init_shotgun_base_def_()


class AbsSsnRsvUnitAction(
    AbsSsnGenerForResolver,
    AbsSsnRsvUnitDef,
    AbsSsnShotgunBaseDef
):
    def __init__(self, *args, **kwargs):
        super(AbsSsnRsvUnitAction, self).__init__(*args, **kwargs)
        #
        rsv_obj = args[0]
        if self.get_is_loadable():
            self._set_rsv_unit_def_init_(rsv_obj, self._configure)
            self._init_shotgun_base_def_()

    def get_is_visible(self):
        if self.rsv_unit is not None:
            step_includes = self.configure.get(
                'resolver.step_includes'
            )
            if step_includes:
                step = self.rsv_unit.get('step')
                if step not in step_includes:
                    return False
        return True

    def get_is_executable(self):
        if self.rsv_unit is not None:
            step_includes = self.configure.get(
                'resolver.step_includes'
            )
            if step_includes:
                step = self.rsv_unit.get('step')
                if step not in step_includes:
                    return False
            #
            result = self.rsv_unit.get_result(
                version=self.rsv_unit_version,
                variants_extend=self.rsv_unit_extend_variants
            )
            if result:
                return True
            return False
        return False


class AbsSsnOptionExecuteDef(object):
    EXECUTOR = None

    @classmethod
    def _get_rsv_task_version_(cls, rsv_scene_properties):
        if rsv_scene_properties.get('shot'):
            return '{project}.{shot}.{step}.{task}.{version}'.format(**rsv_scene_properties.value)
        elif rsv_scene_properties.get('asset'):
            return '{project}.{asset}.{step}.{task}.{version}'.format(**rsv_scene_properties.value)
        else:
            raise TypeError()

    #
    def _set_option_execute_def_init_(self, configure):
        self._ddl_configure = configure
        self._ddl_job_id = None

    def get_ddl_configure(self):
        return self._ddl_configure

    def find_dependent_ddl_job_ids(self, *args, **kwargs):
        pass

    def get_executor(self):
        return self.EXECUTOR(
            self
        )

    def set_execute_by_deadline(self):
        executor = self.get_executor()
        return executor.execute_with_deadline()

    def set_ddl_job_id(self, ddl_job_id):
        self._ddl_job_id = ddl_job_id

    def get_ddl_job_id(self):
        return self._ddl_job_id

    def set_execute_by_shell(self, block=False):
        executor = self.get_executor()
        executor.set_run_with_shell(block)

    def get_shell_script_command(self):
        return self.get_executor().get_shell_command()


class AbsSsnOptionGui(
    bsc_session.AbsSsnGener,
    AbsSsnOptionExecuteDef
):
    def __init__(self, *args, **kwargs):
        if 'option' in kwargs:
            self._option_opt = bsc_core.ArgDictStringOpt(
                kwargs.pop('option')
            )
        else:
            self._option_opt = None
        #
        super(AbsSsnOptionGui, self).__init__(*args, **kwargs)
        #
        if self._option_opt is not None:
            self.__set_option_completion_()
            #
            self._set_option_execute_def_init_(
                self._configure.get_as_content('hook_option.deadline')
            )

    def __set_option_completion_(self):
        option_opt = self.get_option_opt()
        #
        hook_engine = self._configure.get('hook_option.engine')
        option_opt.set('hook_engine', hook_engine)

    def get_option_opt(self):
        return self._option_opt

    option_opt = property(get_option_opt)

    def get_option(self):
        return self._option_opt.to_string()

    option = property(get_option)


class AbsSsnDatabaseOptionAction(
    bsc_session.AbsSsnOptionGener
):
    def __init__(self, *args, **kwargs):
        super(AbsSsnDatabaseOptionAction, self).__init__(*args, **kwargs)

    def get_database_opt(self, disable_new_connection=False):
        return bsc_database.DtbOptForResource(
            self.option_opt.get('database_configure'),
            self.option_opt.get('database_configure_extend'),
            disable_new_connection=disable_new_connection
        )

    database_opt = property(get_database_opt)

    def get_window(self):
        import lxgui.proxy.core as gui_prx_core

        return gui_prx_core.GuiProxyUtil.find_window_proxy_by_unique_id(
            self.option_opt.get('window_unique_id')
        )


class AbsSsnShellExecuteDef(object):
    EXECUTOR = None

    @property
    def configure(self):
        raise NotImplementedError()

    @property
    def option_opt(self):
        raise NotImplementedError()

    def _set_shell_execute_def_init_(self, configure):
        self.__set_execute_option_completion_()

    def get_executor(self):
        return self.EXECUTOR(
            self
        )

    def set_execute_by_shell(self, block=False):
        self.get_executor().set_run_with_shell(block)

    def get_shell_script_command(self):
        return self.get_executor().get_shell_command()

    def __set_execute_option_completion_(self):
        hook_engine = self.configure.get('hook_option.engine')
        self.option_opt.set('hook_engine', hook_engine)
        #
        rez_extend_packages = self.configure.get('hook_option.rez.extend_packages') or []
        if rez_extend_packages:
            self.option_opt.set('rez_extend_packages', rez_extend_packages)
        #
        rez_add_environs = self.configure.get('hook_option.rez.add_environs') or []


class AbsSsnOptionToolPanel(
    bsc_session.AbsSsnOptionGener,
    AbsSsnShellExecuteDef
):
    def __init__(self, *args, **kwargs):
        super(AbsSsnOptionToolPanel, self).__init__(*args, **kwargs)
        self._set_shell_execute_def_init_(self._configure)


class AbsSsnRsvOptionToolPanel(
    bsc_session.AbsSsnOptionGener,
    AbsSsnShotgunBaseDef,
):
    def __init__(self, *args, **kwargs):
        super(AbsSsnRsvOptionToolPanel, self).__init__(*args, **kwargs)
        #
        self._init_shotgun_base_def_()


# session for deadline job
class AbsSsnOptionMethod(
    bsc_session.AbsSsnOptionGener,
    AbsSsnOptionExecuteDef
):
    STD_KEYS = [
        'user',
        'host',
        'time_tag',
    ]

    def __init__(self, *args, **kwargs):
        super(AbsSsnOptionMethod, self).__init__(*args, **kwargs)
        self._set_system_option_completion_()
        self._set_option_completion_()
        #
        self._set_option_execute_def_init_(
            self._configure.get_as_content('hook_option.deadline')
        )

    def _set_option_completion_(self):
        option_opt = self.get_option_opt()
        #
        hook_engine = self._configure.get('hook_option.engine')
        option_opt.set('hook_engine', hook_engine)
        #
        rez_extend_packages = self._configure.get('hook_option.rez.extend_packages') or []
        if rez_extend_packages:
            option_opt.set('rez_extend_packages', rez_extend_packages)

    def _set_system_option_completion_(self):
        option_opt = self.get_option_opt()
        for i_key in self.STD_KEYS:
            if option_opt.get(i_key) is None:
                option_opt.set(i_key, bsc_core.SysBaseMtd.get(i_key))

    def get_batch_file_path(self):
        option_opt = self.get_option_opt()

        file_path = ssn_core.SsnHookServerMtd.get_file_path(
            user=option_opt.get('user'),
            time_tag=option_opt.get('time_tag'),
        )
        if bsc_storage.StgPathMtd.get_is_exists(file_path) is False:
            raw = dict(
                user=option_opt.get('user'),
                time_tag=option_opt.get('time_tag'),
            )
            bsc_storage.StgFileOpt(file_path).set_write(raw)
            bsc_log.Log.trace_method_result(
                'hook batch-file write',
                'file="{}"'.format(file_path)
            )
        return file_path

    def find_dependent_ddl_job_ids(self, hook_option):
        lis = []
        hook_option_opt = bsc_core.ArgDictStringOpt(
            hook_option
        )
        main_key = hook_option_opt.get('option_hook_key')
        f = self.get_batch_file_path()
        c = ctt_core.Content(value=f)
        #
        dependent_option_hook_keys = hook_option_opt.get(
            'dependencies', as_array=True
        ) or []
        for i_key in dependent_option_hook_keys:
            i_option_hook_key = ssn_core.SsnHookFileMtd.get_hook_abs_path(
                main_key, i_key
            )
            i_ddl_job_id = c.get(
                'deadline.{}.job_id'.format(i_option_hook_key)
            )
            if i_ddl_job_id:
                lis.append(i_ddl_job_id)
        return lis

    def find_ddl_job_id(self, hook_option):
        hook_option_opt = bsc_core.ArgDictStringOpt(
            hook_option
        )
        option_hook_key = hook_option_opt.get('option_hook_key')
        f = self.get_batch_file_path()
        c = ctt_core.Content(value=f)
        #
        keys = [option_hook_key]
        option_hook_key_extend = hook_option_opt.get('option_hook_key_extend', as_array=True)
        if option_hook_key_extend:
            keys.extend(option_hook_key_extend)
        #
        key = '/'.join(keys)
        #
        return c.get(
            'deadline.{}.job_id'.format(key)
        )

    def update_ddl_result(self, hook_option, ddl_job_id):
        hook_option_opt = bsc_core.ArgDictStringOpt(
            hook_option
        )
        option_hook_key = hook_option_opt.get('option_hook_key')
        f = self.get_batch_file_path()
        c = ctt_core.Content(value=f)
        #
        keys = [option_hook_key]
        option_hook_key_extend = hook_option_opt.get('option_hook_key_extend', as_array=True)
        if option_hook_key_extend:
            keys.extend(option_hook_key_extend)
        #
        key = '/'.join(keys)
        c.set(
            'deadline.{}.job_id'.format(key), ddl_job_id
        )
        c.set(
            'deadline.{}.option'.format(key), hook_option
        )
        c.save_to(
            f
        )

    def get_batch_name(self):
        return


class AbsSsnRsvDef(object):
    def _set_rsv_def_init_(self):
        import lxresolver.core as rsv_core

        self._resolver = rsv_core.RsvBase.generate_root()

    def get_resolver(self):
        return self._resolver

    @property
    def resolver(self):
        return self.get_resolver()


class ValidationChecker(object):
    class CheckStatus(object):
        Error = 'error'
        Warning = 'warning'

    def __init__(self, session):
        self._session = session
        #
        self._check_options = {}
        self._check_results = []

    def set_options(self, options):
        self._check_options = options

    def register_node_result(self, obj_path, description, check_group, check_status='error'):
        self._check_results.append(
            dict(
                type='node',
                node=obj_path,
                elements=[],
                description=description,
                group=check_group,
                status=check_status,
            )
        )

    def register_node_components_result(self, obj_path, elements, description, check_group, check_status='error'):
        self._check_results.append(
            dict(
                type='component',
                node=obj_path,
                elements=elements,
                description=description,
                group=check_group,
                status=check_status,
            )
        )

    def register_node_files_result(self, obj_path, elements, description, check_group, check_status='error'):
        self._check_results.append(
            dict(
                type='file',
                node=obj_path,
                elements=elements,
                description=description,
                group=check_group,
                status=check_status,
            )
        )

    def register_node_directories_result(self, obj_path, elements, description, check_group, check_status='error'):
        self._check_results.append(
            dict(
                type='directory',
                node=obj_path,
                elements=elements,
                description=description,
                group=check_group,
                status=check_status,
            )
        )

    def _get_data_file_path_(self):
        file_path = self._session.option_opt.get('file')
        return bsc_storage.StgTmpYamlMtd.get_file_path(
            file_path, 'asset-validator'
        )

    def get_has_history(self):
        pass

    def set_data_restore(self):
        self._check_options = {}
        self._check_results = []

    def set_data_record(self):
        result_file_path = self._get_data_file_path_()
        bsc_storage.StgFileOpt(
            result_file_path
        ).set_write(
            dict(
                check_results=self._check_results
            )
        )

    def get_data(self):
        result_file_path = self._get_data_file_path_()
        print result_file_path
        raw = bsc_storage.StgFileOpt(
            result_file_path
        ).set_read()
        self._check_results = raw['check_results']
        return raw

    def get_is_passed(self):
        return self.get_summary() != 'error'

    def get_summary(self):
        if self._check_options:
            if self._check_results:
                for i in self._check_results:
                    i_status = i['status']
                    if i_status == 'error':
                        return 'error'
                return 'warning'
            return 'passed'
        return 'ignore'

    def get_info(self):
        return self._get_info_by_results_(
            self.get_summary(), self._check_options, self._check_results
        )

    @classmethod
    def _get_info_by_results_(cls, summary, check_options, check_results):
        list_ = []
        #
        if check_options:
            list_.append(
                'validation check options:\n'
            )
            for k, v in check_options.items():
                list_.append(
                    (
                        '    {}: {}\n'
                    ).format(k, ['off', 'on'][v])
                )
        #
        error_count = 0
        warning_count = 0
        if check_results:
            list_.append('validation check results:\n')
            for seq, i in enumerate(check_results):
                i_d = (
                    '    result {index}:\n'
                    '        node: {node}\n'
                    '        group: {group}\n'
                    '        status: {status}\n'
                    '        description: {description}\n'
                ).format(index=seq+1, **i)
                list_.append(i_d)
                i_elements = i['elements']
                if i_elements:
                    list_.append('        elements:\n')
                    for j_element in i_elements:
                        j_d = (
                            '            {type}: {element}\n'
                        ).format(
                            element=j_element, **i
                        )
                        list_.append(j_d)
                i_status = i['status']
                if i_status == 'error':
                    error_count += 1
                elif i_status == 'warning':
                    warning_count += 1
            #
            list_.insert(
                0,
                (
                    'validation check summary： {} ( {} error and {} warning )\n'
                ).format(summary, error_count, warning_count)
            )
        #
        return ''.join(list_)


# session for rsv project deadline job
class AbsSsnRsvProjectOptionMethod(
    AbsSsnOptionMethod,
    AbsSsnRsvDef
):
    def __init__(self, *args, **kwargs):
        super(AbsSsnRsvProjectOptionMethod, self).__init__(*args, **kwargs)
        self._set_rsv_def_init_()

        self._rsv_project = None
        self._rsv_properties = None
        self._rsv_scene_properties = None

        option_opt = self.get_option_opt()

        self._batch_name = option_opt.get('batch_name')
        self._batch_file_path = option_opt.pop('batch_file')
        self._file_path = option_opt.get('file')

        if self._batch_file_path:
            self._rsv_project = self._resolver.get_rsv_project_by_any_file_path(self._batch_file_path)
            self._rsv_scene_properties = self._resolver.get_rsv_scene_properties_by_any_scene_file_path(
                self._batch_file_path
            )
        else:
            if self._file_path:
                self._rsv_project = self._resolver.get_rsv_project_by_any_file_path(self._file_path)
                self._rsv_scene_properties = self._resolver.get_rsv_scene_properties_by_any_scene_file_path(
                    self._file_path
                )
        # check is project file
        if self._rsv_project is None:
            raise RuntimeError(
                'file is not valid for any project'
            )
        # when file is match scene file rule use scene properties
        if self._rsv_scene_properties:
            self._rsv_properties = self._rsv_scene_properties
        else:
            self._rsv_properties = self._rsv_project.properties

        self.__completion_option_by_rsv_properties_()

    def get_ddl_job_name(self):
        return bsc_storage.StgFileOpt(
            self._file_path
        ).get_name_base()

    def get_group(self):
        return self.get_ddl_job_name()

    def get_rsv_project(self):
        return self._rsv_project

    def get_rsv_properties(self):
        return self._rsv_properties

    def __completion_option_by_rsv_properties_(self):
        if self._rsv_properties is not None:
            option_opt = self.get_option_opt()
            for i_key in ['project']:
                if self._rsv_properties.get_key_is_exists(i_key):
                    option_opt.set(
                        i_key, self._rsv_properties.get(i_key)
                    )
        else:
            raise RuntimeError()

    def get_batch_name(self):
        return self._batch_name


# session for rsv task deadline job
class AbsSsnRsvTaskOptionMethod(
    AbsSsnOptionMethod,
    AbsSsnRsvDef
):

    def __init__(self, *args, **kwargs):
        super(AbsSsnRsvTaskOptionMethod, self).__init__(*args, **kwargs)
        self._set_rsv_def_init_()

        self._rsv_scene_properties = None
        self._rsv_task = None

        option_opt = self.get_option_opt()

        self._batch_file_path = option_opt.pop('batch_file')
        self._file_path = option_opt.get('file')
        if self._batch_file_path:
            self._rsv_scene_properties = self.resolver.get_rsv_scene_properties_by_any_scene_file_path(
                self._batch_file_path
            )
            self._rsv_task = self.resolver.get_rsv_task_by_any_file_path(
                self._batch_file_path
            )
        else:
            if self._file_path:
                self._rsv_scene_properties = self.resolver.get_rsv_scene_properties_by_any_scene_file_path(
                    self._file_path
                )
                self._rsv_task = self.resolver.get_rsv_task_by_any_file_path(
                    self._file_path
                )

        self.__completion_option_by_rsv_scene_properties_()
        #
        # print self.get_option_opt()
        # print self.get_option()

        self._validation_checker = ValidationChecker(self)

    def _set_system_option_completion_(self):
        option_opt = self.get_option_opt()
        for i_key in self.STD_KEYS:
            if option_opt.get(i_key) is None:
                option_opt.set(i_key, bsc_core.SysBaseMtd.get(i_key))

    def __completion_option_by_rsv_scene_properties_(self):
        if self._rsv_scene_properties is not None:
            option_opt = self.get_option_opt()
            for i_key in ['project', 'workspace', 'asset', 'shot', 'step', 'task', 'version', 'application']:
                if self._rsv_scene_properties.get_key_is_exists(i_key):
                    option_opt.set(
                        i_key, self._rsv_scene_properties.get(i_key)
                    )
        else:
            raise RuntimeError()

    def get_session_key(self):
        option_opt = self.get_option_opt()
        return ssn_core.SsnHookServerMtd.get_key(
            user=option_opt.get('user'),
            time_tag=option_opt.get('time_tag'),
        )

    def get_batch_file_path(self):
        option_opt = self.get_option_opt()

        file_path = ssn_core.SsnHookServerMtd.get_file_path(
            user=option_opt.get('user'),
            time_tag=option_opt.get('time_tag'),
        )
        if bsc_storage.StgPathMtd.get_is_exists(file_path) is False:
            raw = dict(
                user=option_opt.get('user'),
                time_tag=option_opt.get('time_tag'),
            )
            bsc_storage.StgFileOpt(file_path).set_write(raw)
            bsc_log.Log.trace_method_result(
                'hook batch-file write',
                'file="{}"'.format(file_path)
            )
        return file_path

    def update_ddl_result(self, hook_option, ddl_job_id):
        hook_option_opt = bsc_core.ArgDictStringOpt(
            hook_option
        )
        option_hook_key = hook_option_opt.get('option_hook_key')
        f = self.get_batch_file_path()
        c = ctt_core.Content(value=f)
        #
        keys = [option_hook_key]
        option_hook_key_extend = hook_option_opt.get('option_hook_key_extend', as_array=True)
        if option_hook_key_extend:
            keys.extend(option_hook_key_extend)
        #
        key = '/'.join(keys)
        c.set(
            'deadline.{}.job_id'.format(key), ddl_job_id
        )
        c.set(
            'deadline.{}.option'.format(key), hook_option
        )
        c.save_to(
            f
        )

    def find_ddl_job_id(self, hook_option):
        hook_option_opt = bsc_core.ArgDictStringOpt(
            hook_option
        )
        option_hook_key = hook_option_opt.get('option_hook_key')
        f = self.get_batch_file_path()
        c = ctt_core.Content(value=f)
        #
        keys = [option_hook_key]
        option_hook_key_extend = hook_option_opt.get('option_hook_key_extend', as_array=True)
        if option_hook_key_extend:
            keys.extend(option_hook_key_extend)
        #
        key = '/'.join(keys)
        #
        return c.get(
            'deadline.{}.job_id'.format(key)
        )

    @classmethod
    def get_dependencies(cls, hook_option):
        lis = []
        hook_option_opt = bsc_core.ArgDictStringOpt(
            hook_option
        )
        main_key = hook_option_opt.get('option_hook_key')
        #
        dependent_option_hook_keys = hook_option_opt.get(
            'dependencies', as_array=True
        ) or []
        for i_key in dependent_option_hook_keys:
            i_option_hook_key = ssn_core.SsnHookFileMtd.get_hook_abs_path(
                main_key, i_key
            )
            lis.append(i_option_hook_key)
        return lis

    def find_dependent_ddl_job_ids(self, hook_option):
        lis = []
        hook_option_opt = bsc_core.ArgDictStringOpt(
            hook_option
        )
        main_key = hook_option_opt.get('option_hook_key')
        f = self.get_batch_file_path()
        c = ctt_core.Content(value=f)
        #
        dependent_option_hook_keys = hook_option_opt.get(
            'dependencies', as_array=True
        ) or []
        for i_key in dependent_option_hook_keys:
            i_option_hook_key = ssn_core.SsnHookFileMtd.get_hook_abs_path(
                main_key, i_key
            )
            i_ddl_job_id = c.get(
                'deadline.{}.job_id'.format(i_option_hook_key)
            )
            if i_ddl_job_id:
                lis.append(i_ddl_job_id)
        return lis

    def get_rsv_scene_properties(self):
        return self._rsv_scene_properties

    def get_rsv_task(self):
        return self._rsv_task

    def get_rsv_project(self):
        return self._rsv_task.get_rsv_project()

    def get_rsv_version_name(self):
        return self._get_rsv_task_version_(
            self.get_rsv_scene_properties()
        )

    def get_group(self):
        return self.get_rsv_version_name()

    def get_ddl_name(self):
        return self.get_name()

    def get_executor(self):
        return self.EXECUTOR(
            self
        )

    def get_validation_checker(self):
        return self._validation_checker

    def get_batch_name(self):
        return ''


class AbsOptionRsvTaskBatcherSession(
    AbsSsnRsvTaskOptionMethod
):
    def __init__(self, *args, **kwargs):
        super(AbsOptionRsvTaskBatcherSession, self).__init__(*args, **kwargs)


if __name__ == '__main__':
    print bsc_session.AbsSsnGener._match_fnc_(
        'branch=asset&step=srf',
        {
            "root": "/production/shows",
            "project": "nsa_dev",
            "workspace": "work",
            "workspace_key": "user",
            "branch": "asset",
            "role": "chr",
            "sequence": "",
            "asset": "td_test",
            "shot": "",
            "step": "srf",
            "task": "surface",
            "version": "v000_002",
            "task_extra": "surface",
            "version_extra": "",
            "user": "",
            "artist": "dongchangbao"
        }
    )
