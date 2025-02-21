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
            image_path = bsc_resource.ExtendResource.get('screw/cover/{}.png'.format(resource_type))

        if image_path is not None:
            self._scr_stage.upload_node_preview(node_path, image_path)

        type_path = '/type/{}'.format(resource_type)
        
        # create type assign
        self._scr_stage.create_node_type_assign(node_path, type_path)
        
        # set resource_type
        self._scr_stage.create_or_update_node_parameter(
            node_path, 'resource_type', resource_type
        )
        
        _scr_core.Stage.build_fnc(database_name)

    def new_page(self, resource_type, gui_name, gui_name_chs, image=None):
        index_maximum = self._scr_stage.get_entity_index_maximum(self._scr_stage.EntityTypes.Node)
        database_name = 'resource_{}_{}'.format(resource_type, index_maximum+1)
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

    def get_all_page_data(self):
        dict_ = collections.OrderedDict()

        main_configure = self._scr_stage.get_main_configure()

        type_names = main_configure.get_key_names_at('types')

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

            i_resource_type_name = self._scr_stage.get_node_parameter(i_scr_node_path, 'resource_type')
            if i_resource_type_name not in type_names:
                continue

            i_type_gui_name = main_configure.get('types.{}.gui_name'.format(i_resource_type_name))
            i_type_gui_name_chs = main_configure.get('types.{}.gui_name_chs'.format(i_resource_type_name))

            i_applications = main_configure.get('types.{}.applications'.format(i_resource_type_name))

            if bsc_core.BscApplication.get_is_maya():
                if 'maya' not in i_applications:
                    continue

            dict_[i_node_name] = dict(
                type=dict(
                    name=i_resource_type_name,
                    gui_name=i_type_gui_name,
                    gui_name_chs=i_type_gui_name_chs
                ),
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

        values = main_configure.get_key_names_at('types')

        options = []
        option_names = []
        option_names_chs = []
        for i_value in values:
            if i_value == 'manifest':
                continue

            options.append(i_value)
            i_gui_name = main_configure.get('types.{}.gui_name'.format(i_value))
            i_gui_name_chs = main_configure.get('types.{}.gui_name_chs'.format(i_value))

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




