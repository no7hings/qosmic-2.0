# coding:utf-8
import os

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage


class ImgOiioOptForThumbnail(object):
    COLOR_SPACE_OPTION = {
        'ACEScg_sRGB': '/l/packages/pg/third_party/ocio/aces/1.2/baked/maya/sRGB_for_ACEScg_Maya.csp',
        'ACEScg_Rec709': '/l/packages/pg/third_party/ocio/aces/1.2/baked/maya/Rec.709_for_ACEScg_Maya.csp'
    }

    def __init__(self, obj):
        self._obj = obj
        #
        if bsc_core.SysBaseMtd.get_is_windows():
            self._rv_io_path = 'C:/Program Files/Shotgun/*/bin/rvio_hw.exe'
            self._rv_ls_path = 'C:/Program Files/Shotgun/*/bin/rvls.exe'
        elif bsc_core.SysBaseMtd.get_is_linux():
            self._rv_io_path = '/opt/rv/bin/rvio'
            self._rv_ls_path = '/opt/rv/bin/rvls'
        else:
            raise SystemError()

    def convert_to(self, output_file_path=None, color_space='Linear'):
        if os.path.isfile(self._rv_io_path):
            arguments = [self._rv_io_path]
            #
            input_file_path = self._obj.path
            input_file_path_base = self._obj.path_base
            input_ext = self._obj.ext
            if output_file_path is None:
                output_file_path = '{}{}'.format(input_file_path_base, '.mov')
            #

            output_file = bsc_storage.StgFileOpt(output_file_path)
            output_ext = output_file.get_ext()
            output_file.create_directory()
            #
            arguments += [
                '"{}"'.format(input_file_path),
                '-quality', '1.0', '-scale', '1.0', '-o',
                '"{}"'.format(output_file_path),

            ]
            if color_space in ['ACES CG']:
                arguments += [
                    '-dlut "{}"'.format(
                        bsc_storage.StgPathMapper.map_to_current(
                            self.COLOR_SPACE_OPTION['ACEScg_sRGB']
                        )
                    )
                ]
            #

            bsc_core.PrcBaseMtd.execute_with_result(
                ' '.join(arguments)
            )
            bsc_log.Log.trace_method_result(
                'dot-mov-convert',
                u'file="{}"'.format(output_file_path)
            )
        else:
            bsc_log.Log.trace_method_warning(
                'dot-mov-convert',
                u'bin="{}" is non-exists'.format(self._rv_io_path)
            )

    def get_mov_message(self):
        if os.path.isfile(self._rv_ls_path):
            arguments = [self._rv_ls_path]
            if self._obj.get_is_exists() is True:
                arguments += ['-x', '"{}"'.format(self._obj.path)]
                bsc_core.PrcBaseMtd.execute_with_result(
                    ' '.join(arguments)
                )


class StgImageOpt(object):
    COLOR_SPACE_OPTION = {
        'ACEScg_sRGB': '/l/packages/pg/third_party/ocio/aces/1.2/baked/maya/sRGB_for_ACEScg_Maya.csp',
        'ACEScg_Rec709': '/l/packages/pg/third_party/ocio/aces/1.2/baked/maya/Rec.709_for_ACEScg_Maya.csp'
    }

    def __init__(self, obj):
        self._obj = obj
        #
        if bsc_core.SysBaseMtd.get_is_windows():
            self._rv_io_path = 'C:/Program Files/Shotgun/*/bin/rvio_hw.exe'
            self._rv_ls_path = 'C:/Program Files/Shotgun/*/bin/rvls.exe'
        elif bsc_core.SysBaseMtd.get_is_linux():
            self._rv_io_path = '/opt/rv/bin/rvio'
            self._rv_ls_path = '/opt/rv/bin/rvls'
        else:
            raise SystemError()


class AbsStgObjOpt(object):
    def __init__(self, *args):
        if args[0] is None:
            raise RuntimeError(
                'entity "None" is not available'
            )
        self._stg_obj_query = args[0]

    def get_stg_connector(self):
        return self._stg_obj_query._stg_connector

    connector = property(get_stg_connector)

    def get_shogun(self):
        return self._stg_obj_query.shotgun

    shotgun = property(get_shogun)

    @property
    def query(self):
        return self._stg_obj_query

    def __str__(self):
        return self._stg_obj_query.__str__()


class StgProjectOpt(AbsStgObjOpt):
    def __init__(self, stg_obj_query):
        super(StgProjectOpt, self).__init__(stg_obj_query)

    def get_color_space(self):
        return self._stg_obj_query.get('sg_colorspace') or 'Linear'

    def set_stg_asset_create(self, **kwargs):
        self.shotgun.create_stg_resource(**kwargs)


class StgResourceOpt(AbsStgObjOpt):
    def __init__(self, *args, **kwargs):
        super(StgResourceOpt, self).__init__(*args, **kwargs)

    def get_cc_stg_users(self):
        return self._stg_obj_query.get('addressings_cc') or []

    def get_stg_tasks(self, stg_steps=None):
        filters = [
            ['entity', 'is', self._stg_obj_query.stg_obj]
        ]
        # when "stg_steps" argument type is list, use step filter mode
        if isinstance(stg_steps, list):
            # when "stg_steps" is [] return []
            if not stg_steps:
                return []
            filters.append(
                ['step', 'in', stg_steps]
            )
        return self.shotgun.find(
            entity_type='Task',
            filters=filters
        )

    def get_stg_shots(self):
        if self.query.type == 'Asset':
            return self._stg_obj_query.get(
                'shots'
            )

    def get_shot_stg_tasks(self, stg_steps=None):
        list_ = []
        if self.query.type == 'Asset':
            stg_shots = self.get_stg_shots()
            for i_stg_shot in stg_shots:
                i_filters = [
                    ['entity', 'is', i_stg_shot]
                ]
                # when "stg_steps" argument type is list, use step filter mode
                if isinstance(stg_steps, list):
                    # when "stg_steps" is [] return []
                    if not stg_steps:
                        return []
                    i_filters.append(
                        ['step', 'in', stg_steps]
                    )
                i_stg_tasks = self.shotgun.find(
                    entity_type='Task',
                    filters=i_filters
                )
                list_.extend(i_stg_tasks)
        return list_


class StgStepOpt(AbsStgObjOpt):
    def __init__(self, stg_obj_query):
        super(StgStepOpt, self).__init__(stg_obj_query)

    def get_downstream_stg_steps(self):
        ids = self._stg_obj_query.get('sg_downstream_ids')
        if ids:
            return [self.connector.get_stg_step(id=i) for i in ids.split(',')]
        return []

    def get_notice_stg_users(self):
        return self._stg_obj_query.get('sg_notice_to_people')


class StgTaskOpt(AbsStgObjOpt):
    def __init__(self, stg_obj_query):
        super(StgTaskOpt, self).__init__(stg_obj_query)

    def append_assign_stg_user(self, stg_user):
        if stg_user is None:
            raise RuntimeError()
        self._stg_obj_query.set_stg_obj_append(
            'task_assignees', stg_user
        )

    def get_stg_status(self):
        return self._stg_obj_query.get('sg_status_list')

    def get_last_stg_version(self):
        return self._stg_obj_query.get('sg_last_version')

    def set_last_stg_version(self, stg_version):
        self._stg_obj_query.set('sg_last_version', stg_version)

    def get_assign_stg_users(self):
        return self._stg_obj_query.get('task_assignees') or []

    def get_cc_stg_users(self):
        # print [self._stg_obj_query._stg_connector.to_query(i).get('name').decode('utf-8') for i in stg_users_assign+stg_users_cc]
        return self._stg_obj_query.get('addressings_cc') or []

    def get_notice_stg_users(self):
        list_ = []
        stg_steps = []
        stg_tasks = []
        c = self.connector
        # task
        stg_task = self.query.stg_obj
        stg_tasks.append(stg_task)
        # step
        stg_step = self.query.get('step')
        stg_steps.append(stg_step)
        stg_step_o = StgStepOpt(c.to_query(stg_step))
        #   downstream steps notice
        downstream_stg_steps = stg_step_o.get_downstream_stg_steps()
        stg_steps.extend(downstream_stg_steps)
        # resource
        stg_resource = self.query.get('entity')
        stg_resource_o = StgResourceOpt(c.to_query(stg_resource))
        #   resource cc
        resource_cc_stg_users = stg_resource_o.get_cc_stg_users()
        list_.extend(resource_cc_stg_users)
        #   downstream tasks
        resource_downstream_stg_tasks = stg_resource_o.get_stg_tasks(
            stg_steps=downstream_stg_steps
        )
        stg_tasks.extend(resource_downstream_stg_tasks)
        if stg_resource['type'] == 'Asset':
            shot_downstream_stg_tasks = stg_resource_o.get_shot_stg_tasks(
                stg_steps=downstream_stg_steps
            )
            stg_tasks.extend(shot_downstream_stg_tasks)
        # all step notice
        for i_stg_step in stg_steps:
            i_stg_step_o = StgStepOpt(c.to_query(i_stg_step))
            i_step_notice_stg_user = i_stg_step_o.get_notice_stg_users()
            list_.extend(i_step_notice_stg_user)
        # all task assign and cc
        for i_stg_task in stg_tasks:
            i_stg_task_o = StgTaskOpt(c.to_query(i_stg_task))
            i_task_assign_stg_users = i_stg_task_o.get_assign_stg_users()
            list_.extend(i_task_assign_stg_users)
            i_task_cc_stg_users = i_stg_task_o.get_cc_stg_users()
            list_.extend(i_task_cc_stg_users)
        return list_


class StgVersionOpt(AbsStgObjOpt):
    def __init__(self, stg_obj_query):
        super(StgVersionOpt, self).__init__(stg_obj_query)

    def get_stg_tags(self):
        return self._stg_obj_query.get('tags') or []

    def append_stg_tags_(self, stg_tag):
        self._stg_obj_query.set_stg_obj_append(
            'tags', stg_tag
        )

    def get_description(self):
        return self._stg_obj_query.get('description')

    def set_description(self, description):
        self._stg_obj_query.set('description', description)

    def set_folder(self, directory_path):
        directory_path_windows = bsc_storage.StgPathMapper.map_to_windows(directory_path)
        directory_path_linux = bsc_storage.StgPathMapper.map_to_linux(directory_path)
        stg_folder = {
            'name': bsc_storage.StgFileOpt(directory_path).name,
            'local_path': directory_path,
            'local_path_windows': directory_path_windows,
            'local_path_linux': directory_path_linux
        }
        self.set_stg_folder(stg_folder)

    def set_publish_directory(self, directory_path):
        directory_path_linux = bsc_storage.StgPathMapper.map_to_linux(directory_path)
        self._stg_obj_query.set('sg_published_path', directory_path_linux)

    def set_stg_folder(self, stg_folder):
        self._stg_obj_query.set('sg_version_folder', stg_folder)

    def get_stg_folder(self):
        return self._stg_obj_query.get('sg_version_folder')

    def set_stg_version_number(self, number):
        self._stg_obj_query.set('sg_version_number', str(number))

    def get_stg_type(self):
        return self._stg_obj_query.get('sg_version_type')

    def set_stg_type(self, stg_type):
        if stg_type:
            self._stg_obj_query.set('sg_version_type', stg_type)
            bsc_log.Log.trace_method_result(
                'stg-version set',
                u'stg-type="{}"'.format(stg_type)
            )

    def set_stg_user(self, stg_user):
        if stg_user:
            self._stg_obj_query.set('user', stg_user)
            bsc_log.Log.trace_method_result(
                'stg-version set',
                u'user="{}"'.format(stg_user)
            )

    def get_stg_user(self):
        return self._stg_obj_query.get('user')

    def set_stg_status(self, stg_status):
        self._stg_obj_query.set('sg_status_list', stg_status)
        bsc_log.Log.trace_method_result(
            'stg-version set',
            u'stg-status="{}"'.format(stg_status)
        )

    def get_stg_status(self):
        return self._stg_obj_query.get('sg_status_list')

    def set_stg_todo(self, stg_todo):
        self._stg_obj_query.set('sg_todo', stg_todo)
        bsc_log.Log.trace_method_result(
            'stg-version set',
            u'stg-todo="{}"'.format(stg_todo)
        )

    def get_stg_todo(self):
        return self._stg_obj_query.get('sg_todo')

    def get_stg_movie(self):
        return self._stg_obj_query.get('sg_uploaded_movie')

    def upload_stg_movie(self, file_path):
        if os.path.isfile(file_path):
            self._stg_obj_query.set_upload('sg_uploaded_movie', file_path)
            # todo: use environ map
            self._stg_obj_query.set(
                'sg_path_to_movie',
                file_path.replace(
                    '/l/prod', '${RV_PATHSWAP_ROOT}'
                ).replace(
                    'l:/prod', '${RV_PATHSWAP_ROOT}'
                )
            )
            bsc_log.Log.trace_method_result(
                'stg-version set',
                u'file="{}"'.format(file_path)
            )
        else:
            bsc_log.Log.trace_method_result(
                'stg-version set',
                u'file="{}" is non-exists'.format(file_path)
            )

    def set_log_add(self, text):
        key = 'sg_td_batch_log'
        _ = self._stg_obj_query.get(key) or u''
        if _:
            _ += '\n'+text
        else:
            _ += text

        self._stg_obj_query.set(
            key, _
        )

    def set_link_model_stg_version(self, stg_version):
        self._stg_obj_query.set(
            'sg_model_version', stg_version
        )

    def extend_custom_notice_stg_users(self, stg_users):
        self._stg_obj_query.set_stg_obj_extend(
            'sg_custom_notice', stg_users
        )

    def extend_stg_playlists(self, stg_playlists):
        self._stg_obj_query.set_stg_obj_extend(
            'playlists', stg_playlists
        )

    def update_stg_last_version(self):
        stg_version = self._stg_obj_query._stg_obj
        task_id = stg_version.get('sg_task').get('id')
        stg_connector = self._stg_obj_query._stg_connector
        # link to Last Version
        stg_connector._stg_instance.update(
            'Task', task_id,
            {'sg_last_version': stg_version}
        )

    def get_stg_resource(self):
        return self._stg_obj_query.get('entity')

    def get_stg_resource_query(self):
        return self.connector.to_query(
            self.get_stg_resource()
        )

    def get_stg_task(self):
        return self._stg_obj_query.get('sg_task')

    def get_stg_task_query(self):
        return self.connector.to_query(
            self.get_stg_task()
        )


class StgLookPassOpt(AbsStgObjOpt):
    def __init__(self, stg_obj_query):
        super(StgLookPassOpt, self).__init__(stg_obj_query)

    def set_image_upload(self, file_path):
        if os.path.isfile(file_path):
            self._stg_obj_query.set_upload('image', file_path)
            bsc_log.Log.trace_method_result(
                'stg-look-pass-upload',
                'file="{}"'.format(file_path)
            )
        else:
            bsc_log.Log.trace_method_result(
                'stg-look-pass-upload',
                'file="{}" is non-exists'.format(file_path)
            )

    def set_link_surface_version(self, stg_version):
        self._stg_obj_query.set(
            'sg_surface_version', stg_version
        )

    def set_link_render_stats_file(self, file_path):
        self._stg_obj_query.set_upload(
            'sg_render_stats_file', file_path
        )

    def set_link_render_profile_file(self, file_path):
        self._stg_obj_query.set_upload(
            'sg_render_profile_file', file_path
        )
