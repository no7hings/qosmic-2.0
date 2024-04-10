# coding:utf-8
import six

import collections

import lxcontent.core as ctt_core

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxbasic.extra.methods as bsc_etr_methods

from . import configure as bsc_stg_configure

from . import base as bsc_stg_base


class StgEntityQuery(object):
    def __init__(self, stg_connector, stg_obj):
        self._stg_connector = stg_connector
        self._stg_obj = stg_obj
        self._type = self._stg_obj.get('type')
        self._id = self._stg_obj.get('id')

    @property
    def stg_connector(self):
        return self._stg_connector

    @property
    def shotgun(self):
        return self._stg_connector.shotgun

    #
    @property
    def type(self):
        return self._type

    @property
    def id(self):
        return self._id

    @property
    def stg_obj(self):
        return self._stg_obj

    def get(self, key):
        _ = self.shotgun.find_one(
            entity_type=self.type,
            filters=[
                ['id', 'is', self.id]
            ],
            fields=[key]
        )
        if _:
            return _[key]

    def get_all_keys(self):
        _ = self.shotgun.schema_field_read(
            self.type
        )
        if _:
            return _.keys()
        return []

    def get_all(self):
        _ = self.shotgun.find_one(
            entity_type=self.type,
            filters=[
                ['id', 'is', self.id]
            ],
            fields=self.get_all_keys()
        )
        return _

    def set(self, key, value):
        self.shotgun.update(
            self.type, self.id,
            {key: value}
        )
        bsc_log.Log.trace_method_result(
            'shotgun property set',
            'type="{}", id="{}", property="{}"'.format(
                self.type,
                self.id,
                key
            )
        )

    def set_upload(self, key, value):
        self.shotgun.upload(
            self.type, self.id,
            value,
            field_name=key
        )
        bsc_log.Log.trace_method_result(
            'shotgun entity upload',
            'type="{}", id="{}", property="{}"'.format(
                self.type,
                self.id,
                key
            )
        )

    def set_stg_obj_append(self, key, stg_obj):
        stg_objs = self.get(key) or []
        ids = []
        for i in stg_objs:
            i_id = i['id']
            ids.append(i_id)
        #
        new_id = stg_obj['id']
        if new_id not in ids:
            stg_objs.append(stg_obj)
            self.set(
                key,
                stg_objs
            )

    def set_stg_obj_extend(self, key, stg_objs):
        [self.set_stg_obj_append(key, i) for i in stg_objs]

    def get_storage_name(self):
        return self.get('tank_name')

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __str__(self):
        return '{}(type={}, id={})'.format(
            self.__class__.__name__,
            self.type, self.id
        )

    def __repr__(self):
        return self.__str__()


class StgConnector(object):
    TASK_DATA_CACHE = dict()
    StgEntityTypes = bsc_stg_configure.StgEntityTypes
    #
    STG_ENTITY_QUERY_CLS = StgEntityQuery
    #
    VERSION_NAME_PATTERN = '{resource}.{step.lower()}.{task}.{version}'
    #
    RESOURCE_TYPE_MAPPER = {
        'project': StgEntityTypes.Project,
        #
        'sequence': StgEntityTypes.Sequence,
        #
        'asset': StgEntityTypes.Asset, 'shot': StgEntityTypes.Shot,
    }

    def __init__(self, **kwargs):
        self._stg_instance = bsc_stg_base.StgBase().generate_connection()

    @property
    def shotgun(self):
        return self._stg_instance

    def get_is_valid(self):
        return self._stg_instance is not None

    @classmethod
    def _get_stg_resource_type_(cls, key):
        return cls.RESOURCE_TYPE_MAPPER[key]

    @classmethod
    def _get_rsv_resource_type_(cls, key):
        return {v: k for k, v in cls.RESOURCE_TYPE_MAPPER.items()}[key]

    def to_query(self, stg_entity):
        return self.STG_ENTITY_QUERY_CLS(self, stg_entity)

    def _set_stg_filters_completion_by_tags_(self, filters, **kwargs):
        if 'tags' in kwargs:
            filters.append(
                ['tags', 'in', [self.get_stg_tag(i) for i in kwargs['tags']]]
            )

    def get_stg_entity_scheme(self, stg_type, key):
        _ = self._stg_instance.schema_field_read(
            entity_type=stg_type, field_name=key
        )
        if isinstance(_, dict):
            return ctt_core.Content(value=_)

    def get_stg_projects(self):
        return self._stg_instance.find(
            entity_type=bsc_stg_configure.StgEntityTypes.Project,
            filters=[]
        ) or []

    def get_stg_project_queries(self):
        return [self.STG_ENTITY_QUERY_CLS(self, i) for i in self.get_stg_projects()]

    def get_stg_project(self, **kwargs):
        """
        :param kwargs: project=<project-name>
        :return:
        """
        project = kwargs['project']
        return self._stg_instance.find_one(
            entity_type=bsc_stg_configure.StgEntityTypes.Project,
            filters=[
                ['name', 'is', str(project).upper()]
            ]
        )

    def get_stg_project_query(self, **kwargs):
        """
        :param kwargs:
            project=<project-name>
        :return:
        """
        stg_obj = self.get_stg_project(**kwargs)
        if stg_obj:
            return self.STG_ENTITY_QUERY_CLS(self, stg_obj)

    # tag/role
    def get_stg_role(self, **kwargs):
        pass

    #
    def get_stg_entity_(self, **kwargs):
        pass

    def get_shotgun_entities(self, shotgun_entity_kwargs):
        list_ = []
        _ = self._stg_instance.find(**shotgun_entity_kwargs) or []
        key_pattern = ';'.join(map(lambda x: '{{{}}}'.format(x), shotgun_entity_kwargs.get('fields')))
        for i in _:
            i = {k: (v if v else 'N/a') for k, v in i.items()}
            i_key = key_pattern.format(**i)
            list_.append(i_key.decode('utf-8'))
        return list_

    def get_shotgun_entities_(self, **kwargs):
        list_ = []
        _ = self._stg_instance.find(**kwargs) or []
        for i in _:
            i = {k: (v if v else 'N/a') for k, v in i.items()}
            list_.append(i)
        return list_

    # entity
    def get_stg_resource(self, **kwargs):
        if 'id' in kwargs:
            return self._stg_instance.find_one(
                entity_type=kwargs['type'],
                filters=[
                    ['id', 'is', int(kwargs['id'])],
                ]
            )
        """
        :param kwargs:
            project=<project-name>
            asset=<asset-name>/shot=<shot-name>
        :return:
        """
        if 'asset' in kwargs:
            branch = 'asset'
        elif 'shot' in kwargs:
            branch = 'shot'
        elif 'sequence' in kwargs:
            branch = 'sequence'
        else:
            raise TypeError()
        #
        resource_name = kwargs[branch]
        #
        return self._stg_instance.find_one(
            entity_type=self._get_stg_resource_type_(branch),
            filters=[
                ['project', 'is', self.get_stg_project(**kwargs)],
                ['code', 'is', resource_name]
            ]
        )

    def get_stg_resource_query(self, **kwargs):
        """
        :param kwargs: =StgConnector.get_stg_resource
        :return:
        """
        stg_obj = self.get_stg_resource(**kwargs)
        if stg_obj:
            return self.STG_ENTITY_QUERY_CLS(self, stg_obj)

    def create_stg_resource(self, **kwargs):
        if 'asset' in kwargs:
            branch = 'asset'
        elif 'shot' in kwargs:
            branch = 'shot'
        elif 'sequence' in kwargs:
            branch = 'sequence'
        else:
            raise TypeError()
        #
        exists_stg_entity = self.get_stg_resource(**kwargs)
        if exists_stg_entity:
            return exists_stg_entity
        resource_name = kwargs[branch]
        # role must be defined
        if 'role' not in kwargs:
            raise RuntimeError()
        # create
        _ = self._stg_instance.create(
            self._get_stg_resource_type_(branch),
            dict(
                project=self.get_stg_project(**kwargs),
                code=resource_name,
                sg_asset_type=kwargs['role']
            )
        )
        #
        bsc_log.Log.trace_method_result(
            'shotgun entity create',
            u'stg-{}="{}"'.format(branch, resource_name)
        )
        return _

    def get_stg_resources(self, **kwargs):
        """
        :param kwargs:
            project=<project-name>
            branch=<branch-name> / role=<role-name> / sequence=<sequence-name>
        :return: list(
        )
        """
        filters = [
            ['project', 'is', self.get_stg_project(**kwargs)],
        ]
        if 'branch' in kwargs:
            branches = [kwargs['branch']]
        else:
            if 'role' in kwargs:
                branches = ['asset']
            elif 'sequence' in kwargs:
                branches = ['shot']
            else:
                branches = ['asset', 'shot']
        #
        if 'role' in kwargs:
            filters.append(
                ['sg_asset_type', 'is', kwargs['role']]
            )
        elif 'sequence' in kwargs:
            filters.append(
                ['sg_sequence', 'is', kwargs['sequence']]
            )
        #
        self._set_stg_filters_completion_by_tags_(filters, **kwargs)
        #
        for i_branch in branches:
            return self._stg_instance.find(
                entity_type=self._get_stg_resource_type_(i_branch),
                filters=filters
            )

    def get_stg_resource_queries(self, **kwargs):
        """
        :param kwargs:
            project=<project-name>
            branch=<branch-name>
        :return: list(
        )
        """
        return [
            self.STG_ENTITY_QUERY_CLS(self, i)
            for i in self.get_stg_resources(**kwargs)
        ]

    # step
    def get_stg_steps(self, **kwargs):
        """
        :param kwargs:
            branch=<branch-name>
        :return: [<dict>, ...] or []
        """
        branch = kwargs['branch']
        return self._stg_instance.find(
            entity_type='Step',
            filters=[
                ['entity_type', 'is', self._get_stg_resource_type_(branch)]
            ]
        ) or []

    def get_stg_step_queries(self, **kwargs):
        """
        :param kwargs:
            = self.get_stg_steps
        :return:
        """
        return [self.STG_ENTITY_QUERY_CLS(self, i) for i in self.get_stg_steps(**kwargs)]

    def get_stg_step(self, **kwargs):
        """
        :param kwargs:
            step=<step-name>
        :return:
        """
        if 'id' in kwargs:
            return self._stg_instance.find_one(
                entity_type='Step',
                filters=[
                    ['id', 'is', int(kwargs['id'])],
                ]
            )
        step = kwargs['step']
        step = bsc_etr_methods.EtrBase.get_shotgun_step_name(step)
        kwargs['step'] = step
        #
        results = self._stg_instance.find(
            entity_type='Step',
            filters=[
                ['short_name', 'is', step],
            ],
            fields=['short_name']
        )
        if results:
            results = [i for i in results if i['short_name'] == step]
            if results:
                return results[0]

    def get_stg_step_query(self, **kwargs):
        """
        :param kwargs:
            = self.get_stg_step
        :return:
        """
        stg_obj = self.get_stg_step(**kwargs)
        if stg_obj:
            return self.STG_ENTITY_QUERY_CLS(self, stg_obj)

    def create_stg_step(self, **kwargs):
        raise RuntimeError()

    # task
    def get_stg_tasks(self, **kwargs):
        """
        find tasks filter by entity and step
        :param kwargs:
            asset/sequence/shot=str
            step=str
        :return:
        """
        return self._stg_instance.find(
            entity_type='Task',
            filters=[
                ['entity', 'is', self.get_stg_resource(**kwargs)],
                ['step', 'is', self.get_stg_step(**kwargs)],
            ]
        )

    def get_stg_task_queries(self, **kwargs):
        return [self.STG_ENTITY_QUERY_CLS(self, i) for i in self.get_stg_tasks(**kwargs)]

    def get_stg_task(self, **kwargs):
        """
        :param kwargs:
            project=<project-name>
            asset=<asset-name>/shot=<shot-name>
            step=<step-name>
            task=<task-name>
        :return:
        """
        if 'id' in kwargs:
            return self._stg_instance.find_one(
                entity_type='Task',
                filters=[
                    ['id', 'is', int(kwargs['id'])],
                ]
            )
        #
        task = kwargs['task']
        return self._stg_instance.find_one(
            entity_type='Task',
            filters=[
                ['entity', 'is', self.get_stg_resource(**kwargs)],
                ['step', 'is', self.get_stg_step(**kwargs)],
                ['content', 'is', task],
            ]
        )

    def get_stg_task_query(self, **kwargs):
        stg_obj = self.get_stg_task(**kwargs)
        if stg_obj:
            return self.STG_ENTITY_QUERY_CLS(self, stg_obj)

    def create_stg_task(self, **kwargs):
        """
        :param kwargs:
            project=<project-name>
            asset=<asset-name>/shot=<shot-name>
            step=<step-name>
            task=<task-name>
        :return:
        """
        #
        exists_stg_task = self.get_stg_task(**kwargs)
        if exists_stg_task:
            return exists_stg_task
        #
        task = kwargs['task']
        _ = self._stg_instance.create(
            'Task',
            dict(
                project=self.get_stg_project(**kwargs),
                entity=self.get_stg_resource(**kwargs),
                step=self.get_stg_step(**kwargs),
                content=task
            )
        )
        bsc_log.Log.trace_method_result(
            'shotgun entity create',
            u'task="{}"'.format(task)
        )
        return _

    # user
    def get_stg_user(self, **kwargs):
        if 'id' in kwargs:
            return self._stg_instance.find_one(
                entity_type='HumanUser',
                filters=[
                    ['id', 'is', kwargs['id']]
                ]
            )
        elif 'name' in kwargs:
            return self._stg_instance.find_one(
                entity_type='HumanUser',
                filters=[
                    ['name', 'is', kwargs['name']]
                ]
            )
        # login name
        elif 'user' in kwargs:
            return self._stg_instance.find_one(
                entity_type='HumanUser',
                filters=[
                    ['login', 'is', kwargs['user']]
                ]
            )
        elif 'sg_nickname' in kwargs:
            return self._stg_instance.find_one(
                entity_type='HumanUser',
                filters=[
                    ['sg_nickname', 'is', kwargs['sg_nickname']]
                ]
            )

    def get_stg_user_query(self, **kwargs):
        stg_obj = self.get_stg_user(**kwargs)
        if stg_obj:
            return self.STG_ENTITY_QUERY_CLS(self, stg_obj)

    def get_stg_users(self, **kwargs):
        if 'id' in kwargs:
            return self._stg_instance.find(
                entity_type='HumanUser',
                filters=[
                    ['id', 'in', kwargs['id']]
                ]
            )
        elif 'name' in kwargs:
            return self._stg_instance.find(
                entity_type='HumanUser',
                filters=[
                    ['name', 'in', kwargs['name']]
                ]
            )
        elif 'user' in kwargs:
            return self._stg_instance.find(
                entity_type='HumanUser',
                filters=[
                    ['login', 'in', kwargs['user']]
                ]
            )
        elif 'sg_nickname' in kwargs:
            return self._stg_instance.find(
                entity_type='HumanUser',
                filters=[
                    ['sg_nickname', 'in', kwargs['sg_nickname']]
                ]
            )
        return []

    def get_stg_version(self, **kwargs):
        if 'id' in kwargs:
            return self._stg_instance.find_one(
                entity_type='Version',
                filters=[
                    ['id', 'is', int(kwargs['id'])],
                ]
            )
        #
        if 'asset' in kwargs:
            branch = 'asset'
        elif 'shot' in kwargs:
            branch = 'shot'
        else:
            raise TypeError()
        #
        step = kwargs['step']
        step = bsc_etr_methods.EtrBase.get_shotgun_step_name(step)
        task = kwargs['task']
        version = kwargs['version']
        #
        version_code = bsc_core.PtnParseOpt(self.VERSION_NAME_PATTERN).update_variants_to(
            resource=kwargs[branch],
            step=step,
            task=task,
            version=version
        ).get_value()
        #
        _ = self._stg_instance.find_one(
            entity_type='Version',
            filters=[
                ['project', 'is', self.get_stg_project(**kwargs)],
                ['code', 'is', version_code],
            ]
        )
        return _

    def get_stg_versions(self, **kwargs):
        _ = self._stg_instance.find(
            entity_type='Version',
            filters=[
                # {'type': 'Task', 'id': 20007}
                ['sg_task', 'is', self.get_stg_task(**kwargs)],
            ]
        )
        return _

    def get_stg_version_query(self, **kwargs):
        stg_obj = self.get_stg_version(**kwargs)
        if stg_obj:
            return self.STG_ENTITY_QUERY_CLS(self, stg_obj)

    def create_stg_version(self, **kwargs):
        exists_stg_version = self.get_stg_version(**kwargs)
        if exists_stg_version:
            return exists_stg_version
        #
        if 'asset' in kwargs:
            branch = 'asset'
        elif 'shot' in kwargs:
            branch = 'shot'
        else:
            raise TypeError()
        #
        step = kwargs['step']
        step = bsc_etr_methods.EtrBase.get_shotgun_step_name(step)
        task = kwargs['task']
        version = kwargs['version']
        #
        name = bsc_core.PtnParseOpt(self.VERSION_NAME_PATTERN).update_variants_to(
            resource=kwargs[branch],
            step=step,
            task=task,
            version=version
        ).get_value()
        #
        _ = self._stg_instance.create(
            'Version',
            dict(
                project=self.get_stg_project(**kwargs),
                entity=self.get_stg_resource(**kwargs),
                sg_task=self.get_stg_task(**kwargs),
                #
                code=name,
                #
                user=self.get_stg_user(**kwargs),
            )
        )
        bsc_log.Log.trace_method_result(
            'shotgun entity create',
            u'stg-version="{}"'.format(name)
        )
        return _

    def get_stg_published_file_type(self, **kwargs):
        file_type = kwargs['file_type']
        _ = self._stg_instance.find_one(
            "PublishedFileType",
            [
                ['code', 'is', file_type]
            ]
        )
        if _:
            return _

    def set_stg_published_file_create(self, **kwargs):
        stg_project = self.get_stg_project(**kwargs)
        stg_entity = self.get_stg_resource(**kwargs)
        stg_task = self.get_stg_task(**kwargs)
        stg_version = self.get_stg_version(**kwargs)
        #
        version = kwargs['version']
        version_number = int(version[1:])
        #
        file_path = kwargs['file']
        file_opt = bsc_storage.StgFileOpt(file_path)
        file_name = file_opt.get_name()
        file_ext = file_opt.get_ext()
        if 'file_type' in kwargs:
            file_type = kwargs['file_type']
            stg_file_type = self.get_stg_published_file_type(
                file_type=file_type
            )
        else:
            if file_ext in ['.ma']:
                stg_file_type = self.get_stg_published_file_type(
                    file_type='Maya Ma'
                )
            else:
                raise RuntimeError()
        #
        if file_opt.get_is_file() is True:
            if stg_version:
                _ = self._stg_instance.create(
                    'PublishedFile',
                    {
                        "path": {
                            'local_path': file_path,
                            'link_type': 'local',
                            'name': file_name
                        },
                        "name": file_name,
                        "code": file_name,
                        "published_file_type": stg_file_type,
                        "sg_status_list": "pub",
                        "version": stg_version,
                        "task": stg_task,
                        "project": stg_project,
                        "entity": stg_entity,
                        "path_cache": bsc_storage.StgPathMapper.map_to_current(file_path),
                        "version_number": version_number,
                    }
                )
                bsc_log.Log.trace_method_result(
                    'shotgun entity create',
                    u'stg-published-file="{}"'.format(file_path)
                )
                return _

    def get_stg_published_file(self, **kwargs):
        pass

    def get_stg_tag(self, tag_name):
        _ = self._stg_instance.find_one(
            entity_type='Tag',
            filters=[
                ['name', 'is', tag_name]
            ]
        )
        return _

    def get_stg_tag_force(self, tag_name):
        stg_obj = self.get_stg_tag(tag_name)
        if stg_obj:
            return stg_obj
        return self.set_stg_tag_create(tag_name)

    def set_stg_tag_create(self, tag_name):
        _ = [
            self._stg_instance.create(
                'Tag',
                dict(name=tag_name)
            )
        ]
        bsc_log.Log.trace_method_result(
            'shotgun entity create',
            u'stg-tag="{}"'.format(tag_name)
        )
        return _

    def get_stg_playlist(self, **kwargs):
        _ = self._stg_instance.find_one(
            entity_type='Playlist',
            filters=[
                ['code', 'is', kwargs['playlist']],
                ['project', 'is', self.get_stg_project(**kwargs)],
            ]
        )
        return _

    def get_stg_playlist_force(self, **kwargs):
        stg_obj = self.get_stg_playlist(**kwargs)
        if stg_obj:
            return stg_obj
        return self.set_stg_playlist_create(**kwargs)

    def set_stg_playlist_create(self, **kwargs):
        name = kwargs['playlist']
        _ = self._stg_instance.create(
            'Playlist',
            dict(
                code=name,
                project=self.get_stg_project(**kwargs)
            )
        )
        bsc_log.Log.trace_method_result(
            'shotgun entity create',
            u'stg-playlist="{}"'.format(name)
        )
        return _

    def set_stg_version_movie_update(self, stg_version, movie_file_path):
        task_id = stg_version.get('sg_task').get('id')
        #
        self._stg_instance.upload(
            'Version', stg_version.get('id'),
            movie_file_path,
            field_name='sg_uploaded_movie'
        )
        # link to Last Version
        self._stg_instance.update(
            'Task', task_id,
            {'sg_last_version': stg_version}
        )
        bsc_log.Log.trace_method_result(
            'stg-version-movie-update',
            u'file="{}"'.format(movie_file_path)
        )

    # look-pass
    def get_stg_look_pass(self, **kwargs):
        look_pass_code = kwargs['look_pass_code']
        return self._stg_instance.find_one(
            entity_type='CustomEntity06',
            filters=[
                ['project', 'is', self.get_stg_project(**kwargs)],
                ['code', 'is', look_pass_code]
            ]
        )

    def get_stg_look_pass_query(self, **kwargs):
        stg_obj = self.get_stg_look_pass(**kwargs)
        if stg_obj:
            return self.STG_ENTITY_QUERY_CLS(self, stg_obj)

    def set_stg_look_pass_create(self, **kwargs):
        stg_project = self.get_stg_project(**kwargs)
        stg_entity = self.get_stg_resource(**kwargs)
        if stg_project and stg_entity:
            look_pass_code = kwargs['look_pass_code']
            _ = [
                self._stg_instance.create(
                    'CustomEntity06',
                    dict(
                        project=stg_project,
                        sg_asset=stg_entity,
                        code=look_pass_code,
                    )
                )
            ]
            bsc_log.Log.trace_method_result(
                'shotgun entity create',
                'stg-look-pass="{}"'.format(look_pass_code)
            )
            return _

    def get_stg_look_passes(self, **kwargs):
        return self._stg_instance.find(
            entity_type='CustomEntity06',
            filters=[
                ['project', 'is', self.get_stg_project(**kwargs)]
            ]
        ) or []

    def get_stg_look_pass_queries(self, **kwargs):
        return [self.STG_ENTITY_QUERY_CLS(self, i) for i in self.get_stg_look_passes(**kwargs)]

    def get_stg_deadline_render_info_query(self, **kwargs):
        mapper = dict(
            mod='MOD',
            grm='GRM',
            srf='LOOKDEV',
            rig='LOOKDEV',
            ani='ANI',
            cfx='CFX',
            efx='EFX',
            dmt='DMT',
        )
        step = kwargs['step']
        step = bsc_etr_methods.EtrBase.get_shotgun_step_name(step)
        if step in mapper:
            stg_entity = self._stg_instance.find_one(
                entity_type='CustomNonProjectEntity01',
                filters=[
                    ['sg_department', 'is', mapper[step]],
                    ['sg_job_type', 'is', 'Render']
                ]
            )
            if stg_entity is not None:
                stg_entity_query = self.STG_ENTITY_QUERY_CLS(self, stg_entity)
                return stg_entity_query

    def get_stg_all_version_types(self):
        _ = self.get_stg_entity_scheme(
            'Version', 'sg_version_type'
        )
        if _ is not None:
            return _.get('sg_version_type.properties.valid_values.value')

    def get_stg_all_version_status(self):
        _ = self.get_stg_entity_scheme(
            'Version', 'sg_status_list'
        )
        if _ is not None:
            return _.get('sg_status_list.properties.valid_values.value')

    def find_task_id(self, project, resource, task):
        if resource == project:
            stg_task = self._stg_instance.find_one(
                entity_type='Task',
                filters=[
                    ['entity', 'is', self.get_stg_project(project=project)],
                    ['content', 'is', task],
                ]
            )
            if stg_task:
                return stg_task['id']
            return None
        for i_branch in ['asset', 'shot', 'sequence']:
            i_kwargs = {'project': project, i_branch: resource}
            i_stg_resource = self.get_stg_resource(
                **i_kwargs
            )
            if i_stg_resource is None:
                continue
            #
            i_stg_task = self._stg_instance.find_one(
                entity_type='Task',
                filters=[
                    ['entity', 'is', i_stg_resource],
                    ['content', 'is', task],
                ]
            )
            if i_stg_task is None:
                continue
            return i_stg_task['id']

    def find_stg_task(self, **kwargs):
        project = kwargs['project']
        task = kwargs['task']
        if 'asset' in kwargs:
            stg_asset = self.get_stg_resource(
                project=project, asset=kwargs['asset']
            )
            if stg_asset:
                return self._stg_instance.find_one(
                    entity_type='Task',
                    filters=[
                        ['entity', 'is', stg_asset],
                        ['content', 'is', task],
                    ]
                )
        elif 'sequence' in kwargs:
            stg_sequence = self.get_stg_resource(
                project=project, sequence=kwargs['sequence']
            )
            if stg_sequence:
                return self._stg_instance.find_one(
                    entity_type='Task',
                    filters=[
                        ['entity', 'is', stg_sequence],
                        ['content', 'is', task],
                    ]
                )
        elif 'shot' in kwargs:
            stg_shot = self.get_stg_resource(
                project=project, shot=kwargs['shot']
            )
            if stg_shot:
                return self._stg_instance.find_one(
                    entity_type='Task',
                    filters=[
                        ['entity', 'is', stg_shot],
                        ['content', 'is', task],
                    ]
                )
        elif 'resource' in kwargs:
            resource = kwargs['resource']
            for i_branch in ['asset', 'sequence', 'shot']:
                i_kwargs = {'project': project, i_branch: resource}
                i_stg_resource = self.get_stg_resource(
                    **i_kwargs
                )
                if i_stg_resource is None:
                    continue
                #
                i_stg_task = self._stg_instance.find_one(
                    entity_type='Task',
                    filters=[
                        ['entity', 'is', i_stg_resource],
                        ['content', 'is', task],
                    ]
                )
                if i_stg_task is not None:
                    return i_stg_task
        else:
            return self._stg_instance.find_one(
                entity_type='Task',
                filters=[
                    ['entity', 'is', self.get_stg_project(project=project)],
                    ['content', 'is', task],
                ]
            )
        return None

    def get_data_from_task_id(self, task_id):
        task_id = int(task_id)
        # cache for task
        if task_id in StgConnector.TASK_DATA_CACHE:
            return StgConnector.TASK_DATA_CACHE[task_id]
        #
        stg_task = self._stg_instance.find_one(
            entity_type='Task',
            filters=[
                ['id', 'is', task_id]
            ],
            fields=[
                'project', 'entity', 'step', 'content'
            ]
        )
        stg_task_query = self.to_query(stg_task)
        task = stg_task_query.get('content')
        stg_project = stg_task_query.get('project')
        stg_project_query = self.to_query(stg_project)
        project = str(stg_project_query.get('name')).lower()
        stg_step = stg_task_query.get('step')
        stg_step_query = self.to_query(stg_step)
        step = str(stg_step_query.get('short_name')).lower()
        stg_resource = stg_task_query.get('entity')
        stg_resource_query = self.to_query(stg_resource)
        branch = self._get_rsv_resource_type_(stg_resource_query.get('type'))
        if branch in {'project'}:
            data = dict(
                project=project,
                branch=branch,
                resource=project,
                step=step,
                task=task
            )
            data[branch] = project
            StgConnector.TASK_DATA_CACHE[task_id] = data
            return data
        elif branch in {'sequence'}:
            resource = stg_resource_query.get('code')
            data = dict(
                project=project,
                branch=branch,
                resource=resource,
                step=step,
                task=stg_task['content']
            )
            data[branch] = resource
            StgConnector.TASK_DATA_CACHE[task_id] = data
            return data
        elif branch in {'asset', 'shot'}:
            resource = stg_resource_query.get('code')
            data = dict(
                project=project,
                branch=branch,
                resource=resource,
                step=step,
                task=stg_task['content']
            )
            data[branch] = resource
            stg_resource_query = self.to_query(stg_resource)
            if branch == 'asset':
                role = stg_resource_query.get('sg_asset_type')
                data['role'] = role
            elif branch == 'shot':
                stg_sequence = stg_resource_query.get('sg_sequence')
                if stg_sequence is None:
                    raise RuntimeError()
                stg_sequence_query = self.to_query(stg_sequence)
                data['sequence'] = stg_sequence_query.get('code')
            StgConnector.TASK_DATA_CACHE[task_id] = data
            return data

    @classmethod
    def get_current_stg_user(cls):
        return StgConnector().get_stg_user(user=bsc_core.SysBaseMtd.get_user_name())

    @classmethod
    def generate_stg_filter_keys(cls, stg_obj, fields):
        tags = []
        for i_key in fields:
            if isinstance(i_key, six.string_types):
                i_value = stg_obj.get(i_key)
            else:
                i_value = stg_obj.get(i_key.keys()[0])

            if isinstance(i_value, six.string_types):
                tags.append(i_value.decode('utf-8'))
            elif isinstance(i_value, (tuple, list)):
                for j_data in i_value:
                    if isinstance(j_data, six.string_types):
                        tags.append(j_data)
                    # entity
                    elif isinstance(j_data, dict):
                        tags.append(
                            j_data.get('name').decode('utf-8')
                        )
            elif isinstance(i_value, dict):
                tags.append(
                    i_value.get('name').decode('utf-8')
                )
        return list(tags)

    @classmethod
    def generate_stg_gui_args(
        cls, shotgun_entity_kwargs, name_field=None, image_field=None,
        keyword_filter_fields=None, tag_filter_fields=None
    ):
        """
        :param shotgun_entity_kwargs:
            etc.
            {
                'entity_type': 'HumanUser',
                'filters': [['sg_studio', 'is', 'CG'], ['sg_status_list', 'is', 'act']],
                'fields': ['sg_nickname', 'email', 'name']
            }
        :param name_field:
        :param image_field:
        :param keyword_filter_fields:
        :param tag_filter_fields:
        :return:
        """
        if shotgun_entity_kwargs:
            name_field = name_field or 'name'
            image_field = image_field or 'image'
            shotgun_entity_kwargs['fields'].append(name_field)
            shotgun_entity_kwargs['fields'].append(image_field)
            if isinstance(tag_filter_fields, (tuple, list)):
                for i_tag in tag_filter_fields:
                    if isinstance(i_tag, six.string_types):
                        shotgun_entity_kwargs['fields'].append(i_tag)
            #
            stg_entities = cls().get_shotgun_entities_(
                **shotgun_entity_kwargs
            )
            stg_entity_dict = {}
            names = []
            image_url_dict = {}
            keyword_filter_dict = collections.OrderedDict()
            tag_filter_dict = collections.OrderedDict()
            for i_stg_entity in stg_entities:
                i_key = i_stg_entity[name_field].decode('utf-8')
                stg_entity_dict[i_key] = i_stg_entity
                names.append(i_key)
                #
                i_image_url = i_stg_entity.get(image_field)
                image_url_dict[i_key] = i_image_url
                if keyword_filter_fields:
                    i_filter_keys = cls.generate_stg_filter_keys(
                        i_stg_entity, keyword_filter_fields
                    )
                    keyword_filter_dict[i_key] = i_filter_keys
                #
                if tag_filter_fields:
                    i_filter_keys = cls.generate_stg_filter_keys(
                        i_stg_entity, tag_filter_fields
                    )
                    i_filter_keys.insert(0, 'All')
                    tag_filter_dict[i_key] = i_filter_keys
            #
            names = bsc_core.RawTextsMtd.sort_by_initial(names)
            return stg_entity_dict, names, image_url_dict, keyword_filter_dict, tag_filter_dict
