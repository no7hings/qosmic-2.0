# coding:utf-8
from __future__ import print_function

import tempfile

import collections

import lxbasic.core as bsc_core

import lxbasic.resource as bsc_resource

from .. import core as _scr_core


class ManifestStageOpt(object):
    @classmethod
    def create_test_pages(cls):
        opt = cls()

        for i_page_name, i_resource_type, i_gui_name, i_gui_name_chs in [
            ('audio_test', 'audio', 'Audio (Test)', '音频（测试）'),
            ('video_test', 'video', 'Video (Test)', '视频（测试）'),
            ('motion_test', 'motion', 'Motion (Test)', '动作（测试）'),
            ('motion_splice', 'motion', 'Motion (Splice)', '动作（拼接）'),
            ('asset_test', 'asset', 'Asset (Test)', '资产（测试）'),
        ]:
            opt.create_or_update_page(
                i_resource_type, i_page_name, i_gui_name, i_gui_name_chs
            )

    @classmethod
    def test_create_page(cls):
        cls().create_or_update_page(
            'video', 'resource_tutorial', 'Tutorial', '教程'
        )

    @classmethod
    def create(cls):
        scr_stage = _scr_core.Stage('resource_manifest')
        _scr_core.Stage.build_fnc('resource_manifest', configure_key='manifest')

        scr_stage.update_all_entity_types()
        scr_stage.update_types(configure_key='manifest')
        scr_stage.update_tags(configure_key='manifest')

    def __init__(self):
        self._scr_stage = _scr_core.Stage(
            'resource_manifest',
        )

    def create_or_update_page(self, resource_type, database_name, gui_name, gui_name_chs, image=None):
        node_path = '/{}'.format(database_name)

        self._scr_stage.create_node(
            node_path, gui_name=gui_name, gui_name_chs=gui_name_chs
        )

        # cover
        if image:
            image_path = image
        else:
            image_path = bsc_resource.BscExtendResource.get('screw/cover/{}.png'.format(resource_type))

        if image_path is not None:
            self._scr_stage.upload_node_preview(node_path, image_path)

        scr_type_path = self.create_type_auto(resource_type)
        
        # create type assign
        self._scr_stage.create_node_type_assign(node_path, scr_type_path)
        
        # set resource_type
        self._scr_stage.create_or_update_node_parameter(
            node_path, 'resource_type', resource_type
        )
        
        _scr_core.Stage.build_fnc(database_name)

    def create_type_auto(self, type_name):
        scr_type_path = '/type/{}'.format(type_name)
        main_configure = self._scr_stage.get_main_configure()
        type_args = type_name.split('/')
        if len(type_args) > 1:
            type_group_name = type_args[0]
            type_group_gui_name = main_configure.get('types.{}.gui_name'.format(type_group_name))
            type_group_gui_name_chs = main_configure.get('types.{}.gui_name_chs'.format(type_group_name))
            scr_type_group_path = '/type/{}'.format(type_group_name)
            # type group
            self._scr_stage.create_type(
                scr_type_group_path,
                gui_name=type_group_gui_name, gui_name_chs=type_group_gui_name_chs,
                kind='unavailable',
            )

        type_gui_name = main_configure.get('types.{}.gui_name'.format(type_name))
        type_gui_name_chs = main_configure.get('types.{}.gui_name_chs'.format(type_name))
        # type
        self._scr_stage.create_type(
            scr_type_path, gui_name=type_gui_name, gui_name_chs=type_gui_name_chs,
            kind='unavailable',
        )
        return scr_type_path

    def new_page(self, resource_type, gui_name, gui_name_chs, image=None):
        index_maximum = self._scr_stage.get_entity_index_maximum(self._scr_stage.EntityTypes.Node)
        database_name = 'resource_{}_{}'.format(resource_type.replace('/', '_'), index_maximum+1)
        self.create_or_update_page(
            resource_type, database_name, gui_name, gui_name_chs, image
        )

    @classmethod
    def repair_page(cls, database_name):
        _scr_core.Stage.build_fnc(database_name)

    def get_page_data(self, name):
        if name == 'resource_manifest':
            return dict(
                resource_type='manifest',
                gui_name='Page Manifest',
                gui_name_chs='页面总览',
            )

        scr_node_path = '/{}'.format(name)
        scr_node = self._scr_stage.get_node(scr_node_path)
        if scr_node:
            return dict(
                resource_type=self._scr_stage.get_node_parameter(scr_node_path, 'resource_type'),
                gui_name=scr_node.gui_name,
                gui_name_chs=scr_node.gui_name_chs,
            )
        return dict(
            resource_type='None',
            gui_name='Not Found',
            gui_name_chs='未找到',
        )

    @classmethod
    def get_valid_type_names(cls):
        list_ = []
        main_configure = _scr_core.Stage.get_main_configure()

        keys = main_configure.get_key_names_at('types')
        for i_key in keys:
            i_type = main_configure.get('types.{}.type'.format(i_key))
            if i_type != 'node':
                continue

            i_enable = main_configure.get('types.{}.enable'.format(i_key))
            if i_enable is False:
                continue

            i_applications = main_configure.get('types.{}.applications'.format(i_key))

            if bsc_core.BscApplication.get_is_maya():
                if 'maya' not in i_applications:
                    continue

            list_.append(i_key)
        return list_

    def get_valid_database_names(self):
        list_ = [
            'resource_manifest'
        ]

        main_configure = self._scr_stage.get_main_configure()
        keys = main_configure.get_key_names_at('types')

        scr_nodes = self._scr_stage.find_all(
            entity_type=self._scr_stage.EntityTypes.Node,
            filters=[
                ('type', 'is', 'node'),
                ('lock', 'is', False),
                ('trash', 'is', False),
            ]
        )
        for i_scr_node in scr_nodes:
            i_scr_node_path = i_scr_node.path

            i_type_name = self._scr_stage.get_node_parameter(i_scr_node_path, 'resource_type')
            if i_type_name not in keys:
                continue

            i_enable = main_configure.get('types.{}.enable'.format(i_type_name))
            if i_enable is False:
                continue

            i_applications = main_configure.get('types.{}.applications'.format(i_type_name))

            if bsc_core.BscApplication.get_is_maya():
                if 'maya' not in i_applications:
                    continue

            list_.append(bsc_core.BscNodePathOpt(i_scr_node.path).get_name())
        return list_

    def get_all_page_data(self):
        dict_ = collections.OrderedDict()

        main_configure = self._scr_stage.get_main_configure()

        keys = main_configure.get_key_names_at('types')

        dict_['resource_manifest'] = dict(
            type=dict(
                name='manifest',
                gui_name='Page Manifest',
                gui_name_chs='页面总览',
            ),
            node=dict(
                name='resource_manifest',
                gui_name='Page Manifest',
                gui_name_chs='页面总览',
            )
        )

        scr_nodes = self._scr_stage.find_all(
            self._scr_stage.EntityTypes.Node,
            [
                ('type', 'is', 'node'),
                ('lock', 'is', False),
                ('trash', 'is', False),
            ]
        )
        for i_scr_node in scr_nodes:
            i_scr_node_path = i_scr_node.path
            i_node_name = bsc_core.BscNodePathOpt(i_scr_node_path).get_name()
            i_node_gui_name = i_scr_node.gui_name
            i_node_gui_name_chs = i_scr_node.gui_name_chs

            i_type_name = self._scr_stage.get_node_parameter(i_scr_node_path, 'resource_type')
            if i_type_name not in keys:
                continue

            i_enable = main_configure.get('types.{}.enable'.format(i_type_name))
            if i_enable is False:
                continue

            i_type_args = i_type_name.split('/')
            if len(i_type_args) > 1:
                i_type_group_name = i_type_args[0]
                i_type_group_gui_name = main_configure.get('types.{}.gui_name'.format(i_type_group_name))
                i_type_group_gui_name_chs = main_configure.get('types.{}.gui_name_chs'.format(i_type_group_name))
                i_type_group_dict = dict(
                    name=i_type_group_name,
                    gui_name=i_type_group_gui_name,
                    gui_name_chs=i_type_group_gui_name_chs
                )
            else:
                i_type_group_dict = dict()

            i_type_gui_name = main_configure.get('types.{}.gui_name'.format(i_type_name))
            i_type_gui_name_chs = main_configure.get('types.{}.gui_name_chs'.format(i_type_name))

            i_applications = main_configure.get('types.{}.applications'.format(i_type_name))

            if bsc_core.BscApplication.get_is_maya():
                if 'maya' not in i_applications:
                    continue

            dict_[i_node_name] = dict(
                type=dict(
                    name=i_type_name,
                    gui_name=i_type_gui_name,
                    gui_name_chs=i_type_gui_name_chs
                ),
                type_group=i_type_group_dict,
                node=dict(
                    name=i_node_name,
                    gui_name=i_node_gui_name,
                    gui_name_chs=i_node_gui_name_chs
                )
            )

        return dict_

    @classmethod
    def get_resource_type_gui_args(cls):
        main_configure = _scr_core.Stage.get_main_configure()

        keys = main_configure.get_key_names_at('types')

        options = []
        option_names = []
        option_names_chs = []
        for i_key in keys:
            if i_key == 'manifest':
                continue

            i_type = main_configure.get('types.{}.type'.format(i_key))
            if i_type == 'group':
                continue

            i_enable = main_configure.get('types.{}.enable'.format(i_key))
            if i_enable is False:
                continue

            options.append(i_key)
            i_gui_name = main_configure.get('types.{}.gui_name'.format(i_key))
            i_gui_name_chs = main_configure.get('types.{}.gui_name_chs'.format(i_key))

            option_names.append(i_gui_name)
            option_names_chs.append(i_gui_name_chs)

        return options, option_names, option_names_chs

    def generate_cover_for(self, database_name):
        scr_node_path = '/{}'.format(database_name)
        scr_node = self._scr_stage.get_node(scr_node_path)
        if scr_node:
            scr_stage = _scr_core.Stage(database_name)

            src_nodes = scr_stage.find_all(
                entity_type=scr_stage.EntityTypes.Node,
                filters=[
                    ('type', 'is', 'node'),
                    ('lock', 'is', False),
                    ('trash', 'is', False),
                ]
            )

            image_paths = []
            c_max = 9
            c = 0
            if src_nodes:
                src_nodes.reverse()

                for i_scr_node in src_nodes:
                    i_scr_entity_path = i_scr_node.path
                    i_image_path = scr_stage.get_node_parameter(i_scr_entity_path, 'thumbnail')
                    if i_image_path:
                        image_paths.append(i_image_path)
                        c += 1

                    if c == c_max:
                        break

            if image_paths:
                import lxbasic.cv.core as bsc_cv_core

                image_path_tmp = tempfile.mktemp(suffix='.cover.jpg')

                bsc_cv_core.ImageConcat(image_paths, image_path_tmp).execute()

                self._scr_stage.upload_node_preview(
                    scr_node_path, image_path_tmp
                )
                return True
        return False




