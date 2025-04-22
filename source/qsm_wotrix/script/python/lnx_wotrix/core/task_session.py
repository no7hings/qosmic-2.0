# coding:utf-8
import collections

import copy

import lxbasic.content as bsc_content

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core


class TaskSession(object):

    INSTANCE = None

    def __init__(self, task_parse, variants):
        self._task_parse = task_parse
        self._properties = bsc_content.DictProperties(variants)

    def __str__(self):
        return '{}{}'.format(
            self.__class__.__name__,
            str(self._properties)
        )

    @property
    def task_parse(self):
        return self._task_parse

    def generate_opt_for(self, opt_cls):
        return opt_cls(self, self._properties)

    def update_properties(self, variants):
        self._properties.clear()
        self._properties.update(variants)

    @property
    def properties(self):
        return self._properties

    @property
    def variants(self):
        return self._properties

    @property
    def scan_resource_path(self):
        return self._task_parse.to_scan_resource_path(**self._properties)

    @property
    def task_unit_path(self):
        return self._task_parse.to_wsp_task_unit_path(**self._properties)

    @property
    def scene_src_path(self):
        return self._task_parse.to_wsp_task_unit_scene_path(**self._properties)

    @property
    def resource_type(self):
        return self._properties['resource_type']

    def get_all_task_units(self):
        resource_type = self._properties['resource_type']
        kwargs = copy.copy(self._properties)
        kwargs.pop('task_unit')
        ptn_opt = self.generate_pattern_opt_for(
            '{}-source-task_unit-dir'.format(resource_type), **kwargs
        )
        matches = ptn_opt.find_matches(sort=True)
        if matches:
            return [x['task_unit'] for x in matches]
        return []

    def get_last_version_code(self, application):
        kwargs = dict(self._properties)
        if 'version' in kwargs:
            kwargs.pop('version')

        pattern_opt = self._task_parse.generate_source_task_scene_src_pattern_opt_for(
            application=application,
            **kwargs
        )
        matches = pattern_opt.find_matches(sort=True)
        if matches:
            return int(matches[-1]['version'])
        return 0

    def save_source_task_scene_src(self, *args, **kwargs):
        return False

    def increment_and_save_source_task_scene_src(self, *args, **kwargs):
        return False

    def send_source_task_scene_src(self, application, scene_path, thumbnail_path):
        version_code_latest = self.get_last_version_code(application)
        if version_code_latest > 0:
            version_latest = str(version_code_latest).zfill(3)
            kwargs_latest = dict(self._properties)
            kwargs_latest['version'] = version_latest
            scene_ptn_opt_latest = self._task_parse.generate_source_task_scene_src_pattern_opt_for(
                application=application,
                **kwargs_latest
            )
            scene_path_latest = scene_ptn_opt_latest.get_value()
            if bsc_storage.StgFileOpt(scene_path).get_is_same_to(scene_path_latest):
                if gui_core.GuiUtil.language_is_chs():
                    gui_core.GuiApplication.exec_message_dialog(
                        '已经存在文件：{}。'.format(scene_path_latest),
                        title='发送文件',
                        size=(320, 120),
                        status='warning',
                    )
                else:
                    gui_core.GuiApplication.exec_message_dialog(
                        'File exists: {}'.format(scene_path_latest),
                        title='Send File',
                        size=(320, 120),
                        status='warning',
                    )
                return

        version_new = str(version_code_latest+1).zfill(3)
        kwargs_new = dict(self._properties)
        kwargs_new['version'] = version_new

        scene_ptn_opt_new = self._task_parse.generate_source_task_scene_src_pattern_opt_for(
            application=application,
            **kwargs_new
        )
        scene_path_new = scene_ptn_opt_new.get_value()
        bsc_storage.StgFileOpt(scene_path).copy_to_file(scene_path_new)

        if thumbnail_path is not None:
            thumbnail_ptn_opt_new = self._task_parse.generate_source_task_thumbnail_pattern_opt_for(
                application=application,
                **kwargs_new
            )
            thumbnail_path_new = thumbnail_ptn_opt_new.get_value()
            bsc_storage.StgFileOpt(thumbnail_path).copy_to_file(thumbnail_path_new)

        if gui_core.GuiUtil.language_is_chs():
            gui_core.GuiApplication.exec_message_dialog(
                '发送文件：{}。'.format(scene_ptn_opt_new),
                title='发送文件',
                size=(320, 120),
                status='correct',
            )
        else:
            gui_core.GuiApplication.exec_message_dialog(
                'Send file: {}'.format(scene_ptn_opt_new),
                title='Send File',
                size=(320, 120),
                status='correct',
            )

    def generate_pattern_opt_for(self, keyword, **kwargs):
        return self._task_parse.generate_pattern_opt_for(keyword, **kwargs)

    def generate_file_variants_for(self, keyword, file_path):
        ptn_opt = self._task_parse.generate_pattern_opt_for(
            keyword
        )
        return ptn_opt.get_variants(file_path, extract=True)

    def get_file_or_dir_for(self, keyword, **kwargs):
        kwargs_new = dict(self._properties)
        kwargs_new.update(**kwargs)
        ptn_opt = self._task_parse.generate_pattern_opt_for(
            keyword, **kwargs_new
        )
        if not ptn_opt.get_keys():
            return ptn_opt.get_value()
        else:
            matches = ptn_opt.find_matches(sort=True)
            if matches:
                return matches[-1]['result']

    def get_file_variants_for(self, keyword, file_path):
        ptn_opt = self._task_parse.generate_pattern_opt_for(
            keyword
        )
        return ptn_opt.get_variants(file_path)

    def get_file_version_args(self, keyword, file_path):
        ptn_opt = self._task_parse.generate_pattern_opt_for(
            keyword
        )
        variants = ptn_opt.get_variants(file_path)
        if variants:
            version = variants['version']

            variants.pop('version')
            ptn_opt.update_variants(**variants)
            matches = ptn_opt.find_matches(sort=True)
            latest = matches[-1]
            version_latest = latest['version']
            return version, version_latest

    def get_latest_file_for(self, keyword, **kwargs):
        kwargs_new = dict(self._properties)
        kwargs_new.update(**kwargs)
        # remove version key latest
        kwargs_new.pop('version')

        ptn_opt = self._task_parse.generate_pattern_opt_for(
            keyword, **kwargs_new
        )

        matches = ptn_opt.find_matches(sort=True)
        if matches:
            return matches[-1]['result']
        return None

    def is_file_match(self, keyword, file_path):
        return bool(self.generate_file_variants_for(keyword, file_path))

    def generate_release_new_version_number(self, **kwargs):
        kwargs_new = dict(self._properties)
        kwargs_new.update(**kwargs)
        resource_type = kwargs_new['resource_type']
        if resource_type == 'asset':
            return self._task_parse.generate_asset_release_new_version_number(
                **kwargs_new
            )
        elif resource_type == 'shot':
            return self._task_parse.generate_shot_release_new_version_number(
                **kwargs_new
            )
        else:
            raise RuntimeError()

    def get_last_release_scene_src_file(self):
        if self.resource_type == 'asset':
            return self.get_latest_file_for(
                'asset-release-maya-scene_src-file'
            )
        elif self.resource_type == 'shot':
            return self.get_latest_file_for(
                'shot-release-maya-scene_src-file'
            )
        else:
            raise RuntimeError()
