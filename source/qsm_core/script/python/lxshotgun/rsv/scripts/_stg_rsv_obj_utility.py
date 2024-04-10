# coding:utf-8
import copy

from urllib import quote, unquote

import datetime

import six

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.shotgun as bsc_shotgun

import lxresolver.core as rsv_core


class RsvStgProjectOpt(object):
    def __init__(self, rsv_project):
        self._resolver = rsv_core.RsvBase.generate_root()
        self._rsv_project = rsv_project
        self._stg_connector = bsc_shotgun.StgConnector()

    def get_default_light_rig_rsv_asset(self):
        properties = self._rsv_project.properties
        project = properties.get('project')
        role = properties.get('roles.light_rig')
        _ = self._stg_connector.get_stg_resource_queries(
            project=project,
            role=role,
            tags=['DefaultRig']
        )
        if _:
            return self._rsv_project.get_rsv_resource(
                role=role,
                asset=_[0].get('code')
            )

    def get_standard_light_rig_rsv_assets(self):
        properties = self._rsv_project.properties
        project = properties.get('project')
        role = properties.get('roles.light_rig')
        _ = self._stg_connector.get_stg_resource_queries(
            project=project,
            role=role,
            tags=['StandardRig']
        )
        if _:
            rsv_assets = [
                self._rsv_project.get_rsv_resource(
                    role=role,
                    asset=i.get('code')
                )
                for i in _
            ]
            rsv_assets = [i for i in rsv_assets if i is not None]
            default_rsv_asset = self.get_default_light_rig_rsv_asset()
            if default_rsv_asset in rsv_assets:
                rsv_assets.remove(default_rsv_asset)
            #
            rsv_assets.insert(0, default_rsv_asset)
            return rsv_assets
        return []

    def get_light_args(self):
        properties = self._rsv_project.properties
        project = properties.get('project')
        role = properties.get('roles.light_rig')
        _0 = self._stg_connector.get_stg_resource_queries(
            project=project,
            role=role,
            tags=['DefaultRig']
        )
        _1 = self._stg_connector.get_stg_resource_queries(
            project=project,
            role=role,
            tags=['StandardRig']
        )
        return [i.get('code') for i in _0], [i.get('code') for i in _1]


class RsvStgTaskOpt(object):
    def __init__(self, rsv_task):
        self._rsv_task = rsv_task
        self._stg_connector = bsc_shotgun.StgConnector()

    def get_version_name(self, version):
        p = self._rsv_task.properties
        return '{project}.{resource}.{step}.{task}.{version}'.format(
            **dict(
                project=p.get('project'),
                resource=p.get(p.get('branch')),
                step=p.get('step'),
                task=p.get('task'),
                version=version,
            )
        )

    def get_stg_version(self, version):
        kwargs = copy.copy(self._rsv_task.properties.get_value())
        kwargs['version'] = version
        return self._stg_connector.get_stg_version(
            **kwargs
        )

    def create_stg_task(self):
        kwargs = self._rsv_task.properties.value
        #
        stg_project = self._stg_connector.get_stg_project(
            **kwargs
        )
        if stg_project is not None:
            stg_entity = self._stg_connector.get_stg_resource(
                **kwargs
            )
            if stg_entity is None:
                self._stg_connector.create_stg_resource(**kwargs)
            #
            stg_step = self._stg_connector.get_stg_step(
                **kwargs
            )
            if stg_step is not None:
                stg_task = self._stg_connector.get_stg_task(
                    **kwargs
                )
                if stg_task is None:
                    self._stg_connector.create_stg_task(
                        **kwargs
                    )
            else:
                bsc_log.Log.trace_method_error(
                    'shotgun-entity create',
                    'step="{}" is non-exists.'.format(kwargs['step'])
                )
        else:
            bsc_log.Log.trace_method_error(
                'shotgun-entity create',
                'project="{}" is non-exists.'.format(kwargs['project'])
            )

    def create_stg_version(
        self,
        version,
        version_type=None,
        version_status=None,
        movie_file=None,
        user=None,
        description=None,
        todo=None,
        notice=None,
        create_shotgun_playlists=False
    ):
        import lxbasic.extra.methods as bsc_etr_methods
        #
        branch = self._rsv_task.get('branch')
        stg_version_kwargs = self._rsv_task.properties.value_as_copy
        stg_version_kwargs['version'] = version
        #
        stg_task_query = self._stg_connector.get_stg_task_query(
            **stg_version_kwargs
        )
        stg_task_opt = bsc_shotgun.StgTaskOpt(stg_task_query)
        #
        stg_version_query = self._stg_connector.get_stg_version_query(
            **stg_version_kwargs
        )
        if stg_version_query is None:
            self._stg_connector.create_stg_version(
                **stg_version_kwargs
            )
            stg_version_query = self._stg_connector.get_stg_version_query(
                **stg_version_kwargs
            )
        # task set last version
        stg_task_opt.set_last_stg_version(stg_version_query.stg_obj)
        # version
        stg_version_opt = bsc_shotgun.StgVersionOpt(stg_version_query)
        #
        version_rsv_unit = self._rsv_task.get_rsv_unit(
            keyword='{}-release-version-dir'.format(branch)
        )
        version_directory_path = version_rsv_unit.get_result(version=version)
        #
        stg_version_opt.set_publish_directory(
            version_directory_path
        )
        #
        stg_version_opt.set_stg_version_number(
            bsc_core.PtnVersionOpt(version).get_number()
        )
        #
        if version_type:
            stg_version_opt.set_stg_type(version_type)
        #
        if version_status:
            stg_version_opt.set_stg_status(version_status)
        #
        if user:
            stg_user = self._stg_connector.get_stg_user(user=user)
            stg_version_opt.set_stg_user(stg_user)
        #
        if movie_file:
            movie_file_opt = bsc_storage.StgFileOpt(movie_file)
            if movie_file_opt.get_is_exists() is True:
                stg_version_opt.upload_stg_movie(movie_file)
            else:
                bsc_log.Log.trace_method_warning(
                    'shotgun movie upload',
                    'file="{}" is non-exists'.format(movie_file)
                )
        else:
            if not stg_version_opt.get_stg_movie():
                f = '/l/resource/td/media_place_holder/no_prevew.mov'
                f_opt = bsc_storage.StgFileOpt(
                    f
                )
                f_opt.map_to_current()
                if f_opt.get_is_exists() is True:
                    stg_version_opt.upload_stg_movie(f)
        #
        if todo:
            stg_version_opt.set_stg_todo(todo)
        #
        if description:
            # need unquote
            if '///' in description:
                description = description.replace('///', '%')
                stg_version_opt.set_description(unquote(description))
            else:
                stg_version_opt.set_description(description)
        # batch tag
        stg_tag = self._stg_connector.get_stg_tag_force('td-batch')
        stg_version_opt.append_stg_tags_(
            stg_tag
        )
        #
        if create_shotgun_playlists is True:
            date_tag = datetime.datetime.now().strftime('%Y-%m-%d')
            playlist = '{}-{}-Review'.format(
                date_tag, stg_version_kwargs['step'].upper()
            )
            stg_playlist = self._stg_connector.get_stg_playlist_force(
                playlist=playlist, **stg_version_kwargs
            )
            stg_version_opt.extend_stg_playlists(
                [stg_playlist]
            )
        # notice latest, value is list
        if notice:
            stg_users = self._stg_connector.get_stg_users(
                name=notice
            )
            if stg_users:
                stg_version_opt.extend_custom_notice_stg_users(
                    stg_users
                )
                #
                mail_addresses = [
                    self._stg_connector.to_query(i).get('email') for i in stg_users
                ]
                message_receivers = [
                    self._stg_connector.to_query(i).get('login') for i in stg_users
                ]
                if isinstance(description, six.text_type):
                    description = description.encode('utf-8')
                #
                subject = (
                    'Version [{}] is Create'
                ).format(
                    self.get_version_name(version)
                )
                c = ''.join(
                    map(
                        lambda x: '{}: {}\n'.format(x[0], x[1]),
                        [
                            ('ID', '{id}'),
                            ('User', '{user}'),
                            ('Time', '{time}'),
                            ('Type', '{version_type}'),
                            ('Folder', '{folder}'),
                            ('Review', '{review}'),
                            ('Description', '{description}')
                        ]
                    )
                )
                content = c.format(
                    **dict(
                        id=stg_version_query.get('id'),
                        user=user,
                        time=bsc_core.SysBaseMtd.get_time(),
                        version_type=version_type,
                        folder=version_directory_path,
                        review=movie_file or 'N/a',
                        description=description or 'N/a',
                    )
                )
                #
                bsc_etr_methods.EtrBase.send_mail(
                    addresses=mail_addresses,
                    receivers=message_receivers,
                    # addresses=['dongchangbao@papegames.net'],
                    subject=subject,
                    content=content
                )
                bsc_etr_methods.EtrBase.send_feishu(
                    addresses=mail_addresses,
                    receivers=message_receivers,
                    # receivers=['dongchangbao'],
                    subject=subject,
                    content=content
                )
                bsc_etr_methods.EtrBase.send_chat(
                    receivers=message_receivers,
                    # receivers=['dongchangbao'],
                    subject=subject,
                    content='{}\n{}'.format(subject, content)
                )

    def set_stg_description_update(self):
        pass
