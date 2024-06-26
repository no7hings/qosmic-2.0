# coding:utf-8
from .... import core as bsc_core

from ... import abstracts as bsc_etr_abstracts


class EtrBase(bsc_etr_abstracts.AbsEtrBase):
    @classmethod
    def get_base_packages_extend(cls):
        return []

    @classmethod
    def get_builtin_packages_extend(cls):
        return []

    @classmethod
    def get_base_command(cls, args_execute=None, packages_extend=None):
        args = [
            'rez-env',
            ' '.join(packages_extend or []),
            ' '.join(args_execute or [])
        ]
        return ' '.join(args)

    @classmethod
    def packages_completed_to(cls, packages):
        return packages

    @classmethod
    def get_project_environs_extend(cls, project):
        return dict(
            PG_SHOW=project.upper(),
        )

    @classmethod
    def get_task_environs_extend(cls, project, resource, task):
        return dict(
            PG_SHOW=project.upper(),
        )

    @classmethod
    def get_task_environs_extend_(cls, **kwargs):
        if 'project' in kwargs:
            return dict(
                PG_SHOW=kwargs['project'].upper(),
            )
        return dict()

    @classmethod
    def get_shotgun_step_name(cls, step):
        return step

    @classmethod
    def set_project(cls, project):
        bsc_core.EnvExtraMtd.set(
            'PG_SHOW', project.upper()
        )

    @classmethod
    def get_project(cls):
        return (bsc_core.EnvExtraMtd.get(
            'PG_SHOW'
        ) or '').lower()

    @classmethod
    def open_ide(cls, file_path):
        cmd = 'rez-env sublime_text -- sublime_text "{}"'.format(
            file_path
        )
        bsc_core.BscProcess.set_run(cmd)

    @classmethod
    def get_app_execute_mapper(cls, *args, **kwargs):
        return {}

    @classmethod
    def get_application_configure_file(cls, *args, **kwargs):
        return

    @classmethod
    def get_deadline_configure_file(cls, *args, **kwargs):
        return

    @classmethod
    def send_mail(cls, *args, **kwargs):
        bsc_core.MsgBaseMtd.send_mail_(
            addresses=kwargs['addresses'],
            subject=kwargs['subject'],
            content=kwargs.get('content') or '',
        )

    @classmethod
    def send_feishu(cls, *args, **kwargs):
        bsc_core.MsgBaseMtd.send_feishu_(
            receivers=kwargs['receivers'],
            subject=kwargs['subject'],
            content=kwargs.get('content') or '',
        )

    @classmethod
    def send_chat(cls, *args, **kwargs):
        bsc_core.MsgBaseMtd.send_chat_(
            receivers=kwargs['receivers'],
            subject=kwargs['subject'],
            content=kwargs.get('content') or '',
        )

    @classmethod
    def register_version_file_dependency(cls, *args, **kwargs):
        pass
