# coding:utf-8
import copy

import datetime

import sys

import time

import json

import os.path

import random

import peewee

import lxbasic.core as bsc_core

import lxbasic.resource as bsc_resource

import lxbasic.storage as bsc_storage

from .. import database as _database


class DataTypes(object):
    MayaNode = 'maya_node'
    MayaNodeGraph = 'maya_node_graph'
    MayaMaterial = 'maya_material'

    All = [
        MayaNode,
        MayaNodeGraph,
        MayaMaterial,
    ]

    NAME_MAP = {
        MayaNode: 'Maya Node',
        MayaNodeGraph: 'Maya Node-graph',
        MayaMaterial: 'Maya Material'
    }

    NAME_CHS_MAP = {
        MayaNode: 'Maya 节点',
        MayaNodeGraph: 'Maya 节点网络',
        MayaMaterial: 'Maya 材质'
    }


def create_model_with_database(model_class, database_):
    class Meta:
        database = database_

    attrs = {
        '__module__': model_class.__module__,
        'Meta': Meta,
    }

    return type(model_class.__name__, (model_class,), attrs)


class Entity(dict):
    DESCRIPTION_KEYS = [
        ('path', 'Path'),
        ('gui_name', 'Name'),
        ('gui_description', 'Description'),
        ('user', 'User'),
        ('ctime', 'Create Time'),
        ('mtime', 'Modify Time')
    ]
    DESCRIPTION_KEYS_CHS = [
        ('path', '路径'),
        ('gui_name_chs', '名字'),
        ('gui_description_chs', '描述'),
        ('user', '用户'),
        ('ctime', '创建时间'),
        ('mtime', '修改时间')
    ]

    def __init__(self, entity_type, *args, **kwargs):
        self.entity_type = entity_type
        super(Entity, self).__init__(*args, **kwargs)

    def __getattr__(self, item):
        return self.__getitem__(item)  # = self[item]

    def __str__(self):
        return '{}(type="{}", path="{}", id="{}")'.format(
            self.entity_type, self.type, self.path, self.id
        )

    def __repr__(self):
        return '\n'+self.__str__()

    def to_string(self, *args):
        if args:
            keys = args
        else:
            keys = self.keys()
            keys.sort()
        return '\n'.join(['{}: {}'.format(x, bsc_core.auto_string(self[x])) for x in keys])

    def to_description(self, language):
        keys = self.DESCRIPTION_KEYS
        if language == 'chs':
            keys = self.DESCRIPTION_KEYS_CHS
        return '\n'.join(
            ['{}: {}'.format(x[1], bsc_core.auto_string(self[x[0]])) for x in keys]
        )


class Stage(object):

    class EntityTypes:
        Node = _database.Node.__name__
        Type = _database.Type.__name__
        Tag = _database.Tag.__name__
        Assign = _database.Assign.__name__
        Property = _database.Property.__name__
        Connection = _database.Connection.__name__

    PATHSEP = '/'

    TIME_TAGS = [
        'today',
        'yesterday',
        'earlier_this_week',
        'last_week',
        'earlier_this_month',
        'last_month',
        'earlier_this_year',
        'long_time_ago',
    ]

    PTN_DATABASE_PATH = '{root}/lazy-resource/.database/{key}.db'
    DEFAULT_THUMBNAIL_FORMAT = 'jpg'
    DEFAULT_THUMBNAIL_WIDTH_MAXIMUM = 512
    
    class NodePathPattens:
        BaseDir = '{root}/lazy-resource/all/{key}/{node}'

        ThumbnailJpg = BaseDir+'/thumbnail.jpg'
        ThumbnailPng = BaseDir+'/thumbnail.png'

        PreviewDir = '{root}/lazy-resource/all/{key}/{node}/preview'
        PreviewImage = PreviewDir+'/image.{format}'
        PreviewImageSequence = PreviewDir+'/images/image.%04d.{format}'
        PreviewVideo = PreviewDir+'/video.{format}'

        JsonDir = '{root}/lazy-resource/all/{key}/{node}/json'
        Json = JsonDir+'/{tag}.json'

        MayaDir = '{root}/lazy-resource/all/{key}/{node}/maya'
        MayaScene = MayaDir+'/{tag}.ma'

    ROOT = None
    OPTIONS = dict()

    @classmethod
    def get_root(cls):
        if cls.ROOT is not None:
            return cls.ROOT
        root = bsc_core.EnvBaseMtd.get_library_root()
        if root is None:
            raise RuntimeError()
        cls.ROOT = root
        return cls.ROOT

    @classmethod
    def get_options(cls):
        if cls.OPTIONS:
            return cls.OPTIONS
        options = dict(root=cls.get_root())
        cls.OPTIONS = options
        return cls.OPTIONS

    @classmethod
    def get_options_as_copy(cls):
        return copy.copy(cls.get_options())

    @classmethod
    def get_all_keys(cls):
        lst = []
        ptn_opt = bsc_core.BscStgParseOpt(cls.PTN_DATABASE_PATH)
        ptn_opt.update_variants(**cls.get_options())
        for i in ptn_opt.get_matches():
            lst.append(i['key'])
        return lst

    @classmethod
    def get_dtb_path(cls, key):
        copy_options = cls.get_options_as_copy()
        copy_options['key'] = key
        return cls.PTN_DATABASE_PATH.format(**copy_options)

    @classmethod
    def get_configure(cls, key):
        return bsc_resource.RscExtendConfigure.get_as_content('lazy-resource/database/{}'.format(key))

    @classmethod
    def to_expression_str(cls, entity_type, filters):
        list_ = []
        for i_key, i_opt, i_value in filters:
            if i_opt == 'is':
                i_fnc_ = '__eq__'
            elif i_opt == 'is not':
                i_fnc_ = '__ne__'
            elif i_opt == 'in':
                i_fnc_ = 'in_'
            elif i_opt == 'contains':
                i_fnc_ = 'contains'
            elif i_opt == 'startswith':
                i_fnc_ = 'startswith'
            elif i_opt == 'endswith':
                i_fnc_ = 'endswith'
            else:
                raise RuntimeError()

            i_value_ = json.dumps(i_value)
            #
            list_.append('(self.{}.{}.{}({}))'.format(entity_type, i_key, i_fnc_, i_value_))
        return ' & '.join(list_)

    @classmethod
    def to_dtb_entity_old(cls, entity_type):
        if entity_type not in cls.__dict__:
            raise RuntimeError()
        return cls.__dict__[entity_type]

    def to_dtd_entity(self, entity_type):
        if entity_type not in self.__dict__:
            raise RuntimeError()
        return self.__dict__[entity_type]

    @classmethod
    def to_entity(cls, entity_type, data):
        return Entity(entity_type, data)

    def __init__(self, key):
        self._key = key
        self._root = self.get_root()
        self._base_options = dict(
            root=self._root
        )

        self._options = self.get_options_as_copy()
        self._options['key'] = self._key

        dtb_path = self.get_dtb_path(key)
        self._dtb_path = dtb_path
        self._dtb = peewee.SqliteDatabase(dtb_path, thread_safe=True)

        self.connect()

    @property
    def key(self):
        return self._key

    @property
    def dtb(self):
        return self._dtb

    def connect(self):
        self.Node = create_model_with_database(_database.Node, self._dtb)
        self.Type = create_model_with_database(_database.Type, self._dtb)
        self.Tag = create_model_with_database(_database.Tag, self._dtb)
        self.Assign = create_model_with_database(_database.Assign, self._dtb)
        self.Property = create_model_with_database(_database.Property, self._dtb)
        self.Connection = create_model_with_database(_database.Connection, self._dtb)
        self.All = [
            self.Node,
            self.Type,
            self.Tag,
            self.Assign,
            self.Property,
            self.Connection
        ]
        return self._dtb

    def close(self):
        self._dtb.close()

    def initialize(self):
        directory_path = os.path.dirname(self._dtb_path)
        if os.path.exists(directory_path) is False:
            os.makedirs(directory_path)

        self._dtb.create_tables(
            self.All
        )

    def build(self):
        self.initialize()
        key = self._key
        configure = bsc_resource.RscExtendConfigure.get_as_content('lazy-resource/database/{}'.format(key))
        if configure is None:
            raise RuntimeError()

        type_data = configure.get('entities.types')
        for k, v in type_data.items():
            self.create_entity(
                self.EntityTypes.Type, k, **v
            )

        tag_data = configure.get('entities.tags')
        for k, v in tag_data.items():
            self.create_entity(
                self.EntityTypes.Tag, k, **v
            )

        node_data = configure.get('entities.nodes')
        for k, v in node_data.items():
            self.create_entity(
                self.EntityTypes.Node, k, **v
            )

    def build_test(self, asset_type):
        # self.create_node_root_group()
        # self.create_node_group('/{}'.format(asset_type))

        random.seed(0)
        type_paths = [
            x.path for x in self.find_all(
                self.EntityTypes.Type,
                filters=[
                    ('type', 'is', 'node'),
                    ('kind', 'is not', 'unavailable')
                ]
            )
        ]
        tag_paths = [
            x.path for x in self.find_all(
                self.EntityTypes.Tag,
                filters=[
                    ('type', 'is', 'node'),
                    ('kind', 'is not', 'unavailable')
                ]
            )
        ]

        today = datetime.datetime.today()
        maximum = int(time.mktime(today.timetuple()))
        start_of_year = today.replace(month=1, day=1)
        minimum = int(time.mktime(start_of_year.timetuple()))

        ctimes = range(minimum, maximum)

        for i in range(500):
            i_node_path = '/{}/test_{}'.format(asset_type, i)

            self.create_node(i_node_path, ctime=random.choice(ctimes))
            if i % 3:
                for j in range(2):
                    j_type_path = random.choice(type_paths)
                    self.create_assign(i_node_path, j_type_path, type='type_assign')

            if i % 2:
                for j in range(2):
                    j_tag_path = random.choice(tag_paths)
                    self.create_assign(i_node_path, j_tag_path, type='tag_assign')

            self.create_parameter(
                i_node_path,
                'video',
                'Z:/temeporaries/dongchangbao/playblast_tool/test.export.v004.mov'
            )
            self.create_parameter(
                i_node_path,
                'thumbnail',
                'Z:/temeporaries/dongchangbao/playblast_tool/test.export.v004.png'
            )

    # base method
    def find_one(self, entity_type, filters):
        dtb_entity = self.__class__.__dict__[entity_type]
        e_str = self.to_expression_str(
            entity_type, filters
        )
        _ = dtb_entity.select().where(
            eval(e_str)
        )
        if _.exists():
            return self.to_entity(entity_type, _.first().__data__)

    def find_all(self, entity_type, filters=None):
        dtb_entity = self.to_dtd_entity(entity_type)
        if filters:
            e_str = self.to_expression_str(
                 entity_type, filters
            )
            _ = dtb_entity.select().where(
                eval(e_str)
            )
        else:
            _ = dtb_entity.select()
        if _.exists():
            return map(lambda x: self.to_entity(entity_type, x.__data__), _)
        return []

    def find_all_by_ctime_tag(self, entity_type, tag='today', filters=None):
        today = datetime.date.today()
        yesterday = today-datetime.timedelta(days=1)
        start_of_week = today-datetime.timedelta(days=today.weekday())
        start_of_last_week = start_of_week-datetime.timedelta(days=7)
        end_of_last_week = start_of_week-datetime.timedelta(seconds=1)
        start_of_month = today.replace(day=1)
        start_of_last_month = (start_of_month-datetime.timedelta(days=1)).replace(day=1)
        end_of_last_month = start_of_month-datetime.timedelta(seconds=1)
        start_of_year = today.replace(month=1, day=1)
        dtb_entity = self.to_dtd_entity(entity_type)

        conditions = {
            #
            'today': '(dtb_entity.ctime >= today) & (dtb_entity.ctime < today+datetime.timedelta(days=1))',
            # yesterday <= ctime < today
            'yesterday': '(dtb_entity.ctime >= yesterday) & (dtb_entity.ctime < today)',
            # start_of_week <= ctime < yesterday
            'earlier_this_week': '(dtb_entity.ctime >= start_of_week) & (dtb_entity.ctime < yesterday)',
            #
            'last_week': '(dtb_entity.ctime >= start_of_last_week) & (dtb_entity.ctime < end_of_last_week)',
            'earlier_this_month': '(dtb_entity.ctime >= start_of_month) & (dtb_entity.ctime < start_of_last_week)',
            'last_month': '(dtb_entity.ctime >= start_of_last_month) & (dtb_entity.ctime < start_of_month)',
            'earlier_this_year': '(dtb_entity.ctime >= start_of_year) & (dtb_entity.ctime < start_of_last_month)',
            'long_time_ago': '(dtb_entity.ctime < start_of_year)'
        }
        if filters:
            _ = dtb_entity.select().where(
                eval(conditions[tag]+'&'+self.to_expression_str(entity_type, filters))
            )
        else:
            _ = dtb_entity.select().where(
                eval(conditions[tag])
            )
        if _.exists():
            return map(lambda x: self.to_entity(entity_type, x.__data__), _)
        return []

    def is_entity_exists(self, entity_type, path):
        dtb_entity = self.to_dtd_entity(entity_type)
        return dtb_entity.select().where(dtb_entity.path == path).exists()

    def get_entity(self, entity_type, path):
        dtb_entity = self.to_dtd_entity(entity_type)
        _ = dtb_entity.select().where(dtb_entity.path == path)
        if _.exists():
            return self.to_entity(entity_type, _.first().__data__)

    def create_entity(self, entity_type, path, **kwargs):
        dtb_entity = self.to_dtd_entity(entity_type)
        if dtb_entity.select().where(dtb_entity.path == path).exists() is True:
            return self.get_entity(entity_type, path)

        dtb_entity = self.to_dtd_entity(entity_type)
        name = path.split(self.PATHSEP)[-1]
        gui_name = bsc_core.RawTextMtd.to_prettify(name, capitalize=True)
        options = dict(
            path=path,
            gui_name=gui_name,
        )
        options.update(**kwargs)
        _ = dtb_entity.create(**options)
        _.save()
        return self.to_entity(entity_type, _.__data__)

    def update_entity(self, entity_type, path, **kwargs):
        dtb_entity = self.to_dtd_entity(entity_type)
        _ = dtb_entity.select().where(dtb_entity.path == path)
        if _.exists():
            entity = _.first()
            for k, v in kwargs.items():
                exec 'entity.{} = {}'.format(k, json.dumps(v))
            entity.save()

    def create_type_group(self, path, **kwargs):
        options = dict(
            path=path, category='group', type='group', gui_icon_name='database/group'
        )
        options.update(**kwargs)
        return self.create_entity(
            self.EntityTypes.Type, **options
        )

    def create_type(self, path, **kwargs):
        options = dict(
            path=path, category='node', type='node', gui_icon_name='database/group'
        )
        options.update(**kwargs)
        return self.create_entity(
            self.EntityTypes.Type, **options
        )

    # extend method
    def create_node_root_group(self, **kwargs):
        options = dict(
            path='/', category='group', type='root', gui_icon_name='database/all'
        )
        options.update(**kwargs)
        return self.create_entity(
            self.EntityTypes.Node, **options
        )

    def create_node_group(self, path, **kwargs):
        options = dict(
            path=path, category='group', type='group', gui_icon_name='database/group'
        )
        options.update(**kwargs)
        return self.create_entity(
            self.EntityTypes.Node, **options
        )

    def create_node(self, path, **kwargs):
        options = dict(
            path=path, category='node', type='node', gui_icon_name='database/object'
        )
        options.update(**kwargs)
        return self.create_entity(
            self.EntityTypes.Node, **options
        )

    def create_assign(self, path_source, path_target, **kwargs):
        path = '{}->{}'.format(path_source, path_target)
        options = dict(
            path=path,
            source=path_source,
            target=path_target
        )
        options.update(**kwargs)
        return self.create_entity(
            self.EntityTypes.Assign,
            **options
        )

    def create_type_assign(self, path_source, path_target, **kwargs):
        return self.create_assign(
            path_source, path_target, type='type_assign', **kwargs
        )

    def create_tag_assign(self, path_source, path_target, **kwargs):
        return self.create_assign(
            path_source, path_target, type='tag_assign', **kwargs
        )

    def create_property(self, node_path, port, value, **kwargs):
        path = '{}.{}'.format(node_path, port)
        options = dict(
            path=path,
            node=node_path,
            port=port,
            value=value,
        )
        options.update(**kwargs)
        return self.create_entity(
            self.EntityTypes.Property,
            **options
        )

    def update_property(self, node_path, port, value, **kwargs):
        path = '{}.{}'.format(node_path, port)
        self.update_entity(
            self.EntityTypes.Property, path, value=value, **kwargs
        )

    def create_or_update_property(self, node_path, port, value, **kwargs):
        path = '{}.{}'.format(node_path, port)
        if self.is_entity_exists(self.EntityTypes.Property, path) is False:
            self.create_property(
                node_path, port, value, **kwargs
            )
        else:
            self.update_property(
                node_path, port, value, **kwargs
            )

    def create_parameter(self, node_path, port, value, **kwargs):
        return self.create_property(node_path, port, value, type='parameter', **kwargs)

    def create_or_update_parameters(self, node_path, port, value, **kwargs):
        return self.create_or_update_property(node_path, port, value, type='parameter', **kwargs)

    def upload_node_preview(self, node_path, file_path):
        if self.check_node_exists(node_path) is False:
            return False

        file_opt = bsc_storage.StgFileOpt(file_path)
        if file_opt.get_is_file() is False:
            return False

        node_name = bsc_core.BscPathOpt(node_path).name
        options = copy.copy(self._options)
        options['node'] = node_name
        # use jpg default
        thumbnail_path = self.NodePathPattens.ThumbnailJpg.format(**options)
        options['format'] = file_opt.format
        # image
        if file_opt.ext in {'.png', '.jpg', '.tga', '.exr'}:
            image_path = self.NodePathPattens.PreviewImage.format(**options)
            file_opt.copy_to_file(image_path)
            # noinspection PyBroadException
            try:
                # fixme: convert png to jpg?
                bsc_storage.ImgOiioOpt(image_path).convert_to(
                    thumbnail_path
                )
                self.create_or_update_parameters(
                    node_path, 'image', image_path
                )
                self.create_or_update_parameters(
                    node_path, 'thumbnail', thumbnail_path
                )
                return True
            except Exception:
                return False
        # video
        elif file_opt.ext in {'.mov', '.avi', '.mp4'}:
            video_path = self.NodePathPattens.PreviewVideo.format(**options)
            file_opt.copy_to_file(video_path)
            # noinspection PyBroadException
            try:
                self.create_or_update_parameters(
                    node_path, 'video', video_path
                )
                bsc_core.BscFfmpeg.extract_frame(video_path, thumbnail_path, 0)
                self.create_or_update_parameters(
                    node_path, 'thumbnail', thumbnail_path
                )
                thumbnail_sequence_path = bsc_core.BscFfmpeg.extract_all_frames(
                    video_path,
                    image_format=self.DEFAULT_THUMBNAIL_FORMAT,
                    width_maximum=self.DEFAULT_THUMBNAIL_WIDTH_MAXIMUM
                )
                self.create_or_update_parameters(
                    node_path, 'thumbnail_sequence', thumbnail_sequence_path
                )
                return True
            except Exception:
                bsc_core.BscException.print_stack()
                return False

        return False

    def upload_node_preview_as_image_sequence(self, node_path, file_path):
        if self.check_node_exists(node_path) is False:
            return False

        if bsc_storage.StgFileTiles.get_is_exists(file_path) is False:
            return False

        node_name = bsc_core.BscPathOpt(node_path).name
        options = copy.copy(self._options)
        options['node'] = node_name
        file_opt = bsc_storage.StgFileOpt(file_path)
        options['format'] = file_opt.format

        image_sequence_path = self.NodePathPattens.PreviewImageSequence.format(**options)
        thumbnail_path = self.NodePathPattens.ThumbnailJpg.format(**options)

        file_paths = bsc_storage.StgFileTiles.get_tiles(file_path)
        file_paths.sort()
        for i_seq, i_file_path in enumerate(file_paths):
            i_file_path_dst = image_sequence_path.replace('%04d', str(i_seq).zfill(4))
            bsc_storage.StgFileOpt(i_file_path).copy_to_file(i_file_path_dst)

        bsc_storage.StgFileOpt(file_paths[0]).copy_to_file(thumbnail_path)

        self.create_or_update_parameters(
            node_path, 'image_sequence', image_sequence_path
        )
        self.create_or_update_parameters(
            node_path, 'thumbnail', thumbnail_path
        )

    def upload_node_json(self, node_path, tag, data):
        if self.check_node_exists(node_path) is False:
            return False

        node_name = bsc_core.BscPathOpt(node_path).name
        options = copy.copy(self._options)
        options['node'] = node_name
        options['tag'] = tag

        json_path = self.NodePathPattens.Json.format(**options)

        json_opt = bsc_storage.StgFileOpt(json_path)
        json_opt.set_write(data)

        self.create_or_update_parameters(
            node_path, tag, json_path
        )

    def generate_node_json_path(self, node_path, tag):
        node_name = bsc_core.BscPathOpt(node_path).name
        options = copy.copy(self._options)
        options['node'] = node_name
        options['tag'] = tag

        return self.NodePathPattens.Json.format(**options)

    def upload_node_maya_scene(self, node_path, tag, file_path):
        maya_scene_path = self.generate_node_maya_scene_path(node_path, tag)
        file_opt = bsc_storage.StgFileOpt(file_path)
        file_opt.copy_to_file(maya_scene_path)
        self.create_or_update_parameters(
            node_path, tag, maya_scene_path
        )

    def generate_node_maya_scene_path(self, node_path, tag):
        node_name = bsc_core.BscPathOpt(node_path).name
        options = copy.copy(self._options)
        options['node'] = node_name
        options['tag'] = tag
        return self.NodePathPattens.MayaScene.format(**options)

    def generate_node_motion_json_path(self, node_path, tag):
        options = copy.copy(self._options)
        options['node'] = bsc_core.BscPathOpt(node_path).name
        options['tag'] = tag
        return self.NodePathPattens.Json.format(**options)

    def generate_node_base_dir_path(self, node_path):
        options = copy.copy(self._options)
        options['node'] = bsc_core.BscPathOpt(node_path).name
        return self.NodePathPattens.BaseDir.format(**options)

    def get_node(self, path):
        return self.get_entity(
            self.EntityTypes.Node, path
        )

    def get_node_parameter(self, node_path, port):
        path = '{}.{}'.format(node_path, port)
        p = self.get_entity(
            self.EntityTypes.Property, path
        )
        if p:
            return p.value

    def check_node_exists(self, path):
        return self.is_entity_exists(self.EntityTypes.Node, path)


