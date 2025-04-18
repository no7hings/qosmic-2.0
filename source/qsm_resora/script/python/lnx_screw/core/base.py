# coding:utf-8
import copy

import datetime

import time

import json

import random

import peewee

from playhouse import migrate

import six

import threading

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.pinyin as bsc_pinyin

import lxbasic.resource as bsc_resource

import lxbasic.storage as bsc_storage

import qsm_general.core as qsm_gnl_core

from .. import database as _model

from . import mysql as _mysql


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


def generate_entity_type_models(model_class, database_):
    class Meta:
        database = database_

    attrs = {
        '__module__': model_class.__module__,
        'Meta': Meta,
    }

    return type(model_class.__name__, (model_class,), attrs)


class Entity(dict):
    DESCRIPTION_KEYS = [
        # ('path', 'Path'),
        ('gui_name', 'Name'),
        ('gui_description', 'Description'),
        ('user', 'User'),
        ('ctime', 'Create Time'),
        ('mtime', 'Modify Time')
    ]
    DESCRIPTION_KEYS_CHS = [
        # ('path', '路径'),
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
            keys = list(self.keys())
            keys.sort()
        return '\n'.join(['{}: {}'.format(x, bsc_core.ensure_string(self[x])) for x in keys])

    def is_root(self):
        return self.path == '/'

    def to_description(self, language):
        keys = self.DESCRIPTION_KEYS
        if language == 'chs':
            keys = self.DESCRIPTION_KEYS_CHS
        return '\n'.join(
            [
                '{}: {}'.format(
                    x[1],
                    bsc_core.ensure_string(
                        bsc_core.BscTimePrettify.to_prettify_by_timetuple_(
                            self[x[0]].timetuple(), language
                        ) if x[0] in {'ctime', 'mtime'} else self[x[0]]
                    )
                ) for x in keys
            ]
        )


class Stage(object):
    """
# create root user
mysql -u root -p
CREATE USER 'qosmic'@'%' IDENTIFIED WITH mysql_native_password BY 'qosmic';
GRANT ALL PRIVILEGES ON *.* TO 'qosmic'@'%';
FLUSH PRIVILEGES;
    """

    class EntityTypes:
        Node = _model.Node.__name__
        Type = _model.Type.__name__
        Tag = _model.Tag.__name__
        Assign = _model.Assign.__name__
        Property = _model.Property.__name__
        Connection = _model.Connection.__name__

        All = [
            Node,
            Type,
            Tag,
            Assign,
            Property,
            Connection
        ]

    class AssignTypes:
        Type = 'type_assign'
        Tag = 'tag_assign'

    PATHSEP = '/'

    LOCK = threading.Lock()

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

    PTN_SQLITE_DATABASE_PATH = '{root}/lazy-resource/.database/{key}.db'
    PTN_STORAGE_DATA_ROOT_PATH = '{root}/lazy-resource/all/{key}'
    DEFAULT_THUMBNAIL_FORMAT = 'jpg'
    DEFAULT_THUMBNAIL_WIDTH_MAXIMUM = 512

    TIMEOUT = 3600*4
    
    class NodePathPattens:
        BaseDir = '{root}/lazy-resource/all/{key}/{node}'

        ThumbnailJpg = BaseDir+'/thumbnail.jpg'
        ThumbnailPng = BaseDir+'/thumbnail.png'

        PreviewDir = '{root}/lazy-resource/all/{key}/{node}/preview'
        PreviewImage = PreviewDir+'/image.{format}'
        PreviewJpg = PreviewDir+'/image.jpg'
        PreviewImageDir = PreviewDir+'/images'
        PreviewImageSequence = PreviewDir+'/images/image.%04d.{format}'
        PreviewVideo = PreviewDir+'/video.{format}'
        PreviewMov = PreviewDir+'/video.mov'
        PreviewAudio = PreviewDir+'/audio.{format}'
        PreviewMp3 = PreviewDir+'/audio.mp3'
        PreviewAudioPickle = PreviewDir+'/audio.pkl'

        JsonDir = '{root}/lazy-resource/all/{key}/{node}/json'
        Json = JsonDir+'/{node}.{tag}.json'

        MayaDir = '{root}/lazy-resource/all/{key}/{node}/maya'
        MayaScene = MayaDir+'/{node}.{tag}.ma'

        SourceDir = '{root}/lazy-resource/all/{key}/{node}/source'

    ROOT = None
    OPTIONS = dict()

    DTB_CACHE = dict()

    RESOURCE_TYPE_CACHE = dict()
    RESOURCE_TYPE_OPTIONS_CACHE = dict()
    APPLICATIONS_CACHE = dict()

    @classmethod
    def get_root(cls):
        if cls.ROOT is not None:
            return cls.ROOT
        root = bsc_core.BscEnviron.get_library_root()
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
        # todo: remove this method
        return []

    @classmethod
    def get_mysql_configure(cls):
        if qsm_gnl_core.scheme_is_release():
            key = 'lazy/mysql_new'
        else:
            key = 'lazy/mysql'
        return bsc_resource.BscExtendConfigure.get_as_content(key)

    @classmethod
    def get_mysql_options(cls):
        cfg = cls.get_mysql_configure()
        return cfg.get('options')

    @classmethod
    def get_sqlite_dtb_path(cls, key):
        if key in cls.DTB_CACHE:
            return cls.DTB_CACHE[key]

        copy_options = cls.get_options_as_copy()
        copy_options['key'] = key
        _ = cls.PTN_SQLITE_DATABASE_PATH.format(**copy_options)
        cls.DTB_CACHE[key] = _
        return _

    @classmethod
    def get_storage_data_root_path(cls, key):
        copy_options = cls.get_options_as_copy()
        copy_options['key'] = key
        _ = cls.PTN_STORAGE_DATA_ROOT_PATH.format(**copy_options)
        return _

    @classmethod
    def get_configure(cls, configue_key=None):
        if configue_key is not None:
            return cls.get_override_configure(configue_key)
        return cls.get_basic_configure()

    @classmethod
    def get_resource_type(cls, database_name):
        if database_name == 'resource_manifest':
            return 'manifest'

        if database_name in cls.RESOURCE_TYPE_CACHE:
            return cls.RESOURCE_TYPE_CACHE[database_name]

        manifest_scr_stage = Stage(
            'resource_manifest'
        )
        scr_node_path = '/{}'.format(database_name)
        scr_node = manifest_scr_stage.get_node(scr_node_path)
        if scr_node:
            type_name = manifest_scr_stage.get_node_parameter(scr_node_path, 'resource_type')
            cls.RESOURCE_TYPE_CACHE[database_name] = type_name
            return type_name

    @classmethod
    def get_applications(cls, database_name):
        if database_name == 'resource_manifest':
            return ['standalone']

        if database_name in cls.APPLICATIONS_CACHE:
            return cls.APPLICATIONS_CACHE[database_name]

        type_name = cls.get_resource_type(database_name)
        if type_name:
            main_configure = cls.get_main_configure()
            applications = main_configure.get('types.{}.applications'.format(type_name))
            cls.APPLICATIONS_CACHE[database_name] = applications
            return applications

    @classmethod
    def get_basic_configure(cls):
        base_configure = bsc_resource.BscExtendConfigure.get_as_content('screw/basic')
        return base_configure

    @classmethod
    def get_main_configure(cls):
        return bsc_resource.BscExtendConfigure.get_as_content('screw/main')

    @classmethod
    def get_resource_type_options(cls, database_name):
        type_name = cls.get_resource_type(database_name)
        if type_name in cls.RESOURCE_TYPE_OPTIONS_CACHE:
            return cls.RESOURCE_TYPE_OPTIONS_CACHE[type_name]

        main_configure = cls.get_main_configure()
        options = main_configure.get('types.{}'.format(type_name))
        cls.RESOURCE_TYPE_OPTIONS_CACHE[type_name] = options
        return options

    @classmethod
    def get_override_configure(cls, configure_key):
        return bsc_resource.BscExtendConfigure.get_as_content('screw/{}'.format(configure_key))

    @classmethod
    def _to_expression_str(cls, entity_type, filters):
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
            # when value is bool do not use json.dumps
            if isinstance(i_value, bool):
                i_value_ = i_value
            else:
                i_value_ = json.dumps(i_value)

            list_.append('(self.{}.{}.{}({}))'.format(entity_type, i_key, i_fnc_, i_value_))
        return ' & '.join(list_)

    @classmethod
    def to_dtb_entity_old(cls, entity_type):
        if entity_type not in cls.__dict__:
            raise RuntimeError()
        return cls.__dict__[entity_type]

    @classmethod
    def _to_entity(cls, entity_type, data):
        return Entity(entity_type, data)

    def __init__(self, key, database_type='mysql'):
        self._dtb_name = key
        self._dtb_type = database_type
        self._root = self.get_root()
        self._base_options = dict(
            root=self._root
        )

        self._options = self.get_options_as_copy()
        self._options['key'] = self._dtb_name
        self._dtb_key = '{}/{}'.format(self._dtb_type, self._dtb_name)
        if self._dtb_key in self.DTB_CACHE:
            self._dtb = self.DTB_CACHE[self._dtb_key]
        else:
            if self._dtb_type == 'sqlite':
                self._sqlite_dtb_path = self.get_sqlite_dtb_path(self._dtb_name)
                self._dtb = peewee.SqliteDatabase(
                    self._sqlite_dtb_path,
                    thread_safe=True,
                    pragmas=dict(
                        max_open=64,
                        # fixme: error in maya open, do not use "wal" mode
                        # journal_mode='wal',
                        cache_size=-1024*64,
                        synchronous=0,
                        timeout=10000
                    )
                )
            elif self._dtb_type == 'mysql':
                mysql_options = self.get_mysql_options()

                self._dtb = peewee.MySQLDatabase(
                    self._dtb_name,
                    **mysql_options
                )
            else:
                raise RuntimeError()

            self._storage_data_root_path = self.get_storage_data_root_path(self._dtb_name)

            self.DTB_CACHE[self._dtb_key] = self._dtb

        self.connect()

    @property
    def type(self):
        # return self._type
        return self.get_resource_type(self._dtb_name)

    @property
    def resource_type(self):
        return self.get_resource_type(self._dtb_name)

    @property
    def applications(self):
        return self.get_applications(self._dtb_name)

    @property
    def resource_type_options(self):
        return self.get_resource_type_options(self._dtb_name)

    # old usage, use name instance
    @property
    def key(self):
        return self._dtb_name

    @property
    def name(self):
        return self._dtb_name

    @property
    def dtb(self):
        return self._dtb

    @property
    def configure(self):
        return self.get_basic_configure()

    def connect(self):
        self.Node = generate_entity_type_models(_model.Node, self._dtb)
        self.Type = generate_entity_type_models(_model.Type, self._dtb)
        self.Tag = generate_entity_type_models(_model.Tag, self._dtb)
        self.Assign = generate_entity_type_models(_model.Assign, self._dtb)
        self.Property = generate_entity_type_models(_model.Property, self._dtb)
        self.Connection = generate_entity_type_models(_model.Connection, self._dtb)
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

    @classmethod
    def initialize_fnc(cls, database_name):
        _mysql.MySql.create_database(
            cls.get_mysql_options(), database_name
        )
        bsc_storage.StgPath.create_directory(
            cls.get_storage_data_root_path(database_name)
        )

    @classmethod
    def build_fnc(cls, database_name, configure_key=None):
        cls.initialize_fnc(database_name)

        stage = cls(database_name)
        stage.create_entity_types()

        configure = cls.get_configure(configure_key)

        type_data = configure.get('entities.types')
        for k, v in type_data.items():
            stage.create_entity(
                stage.EntityTypes.Type, k, **v
            )

        tag_data = configure.get('entities.tags')
        for k, v in tag_data.items():
            stage.create_entity(
                stage.EntityTypes.Tag, k, **v
            )

        node_data = configure.get('entities.nodes')
        for k, v in node_data.items():
            stage.create_entity(
                stage.EntityTypes.Node, k, **v
            )

    def _to_dtb_entity_type(self, entity_type):
        # fixme: reconnect for timeout?
        if self._dtb.is_closed():
            self._dtb.connect()
        if entity_type not in self.__dict__:
            raise RuntimeError()
        return self.__dict__[entity_type]
        
    def create_entity_types(self):
        self._dtb.create_tables(
            self.All
        )

    def update_entity_type_for(self, entity_type):
        model = self._to_dtb_entity_type(entity_type)

        fields_old = self.get_entity_type_property_keys_old(entity_type)
        fields_new = self.get_entity_type_property_keys_new(entity_type)

        fields_addition = set(fields_new)-set(fields_old)
        if not fields_addition:
            return

        migrator = migrate.MySQLMigrator(self._dtb)
        migrations = []
        for field_name in fields_addition:
            field_object = model._meta.fields[field_name]

            migrations.append(migrator.add_column(entity_type, field_name, field_object))

        if migrations:
            migrate.migrate(*migrations)

    def update_all_entity_types(self):
        for i_entity_type in self.EntityTypes.All:
            self.update_entity_type_for(i_entity_type)

    def get_entity_type_property_keys_old(self, entity_type):
        return [x.name for x in self._dtb.get_columns(entity_type)]

    def get_entity_type_property_keys_new(self, entity_type):
        return [x.name for x in self._to_dtb_entity_type(entity_type)._meta.sorted_fields]

    def update_types(self, configure_key=None):
        configure = self.get_configure(configure_key)
        if configure is None:
            raise RuntimeError()

        tag_data = configure.get('entities.types')
        for k, v in tag_data.items():
            self.update_entity(
                self.EntityTypes.Type, k, **v
            )

    def update_tags(self, configure_key=None):
        configure = self.get_configure(configure_key)
        if configure is None:
            raise RuntimeError()

        tag_data = configure.get('entities.tags')
        for k, v in tag_data.items():
            self.update_entity(
                self.EntityTypes.Tag, k, **v
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
                    self.create_assign(i_node_path, j_type_path, type=self.AssignTypes.Type)

            if i % 2:
                for j in range(2):
                    j_tag_path = random.choice(tag_paths)
                    self.create_assign(i_node_path, j_tag_path, type=self.AssignTypes.Tag)

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
        dtb_entity_type = self._to_dtb_entity_type(entity_type)
        e_str = self._to_expression_str(
            entity_type, filters
        )
        _ = dtb_entity_type.select().where(
            eval(e_str)
        )
        if _.exists():
            return self._to_entity(entity_type, _.first().__data__)

    def _find_all_fnc(self, entity_type, filters=None):
        dtb_entity_type = self._to_dtb_entity_type(entity_type)
        if not filters:
            filters = []
        # trash flag using in GUI
        # filters.append(
        #     ('trash', 'is', 0)
        # )

        if filters:
            e_str = self._to_expression_str(
                 entity_type, filters
            )
            _ = dtb_entity_type.select().where(
                eval(e_str)
            )
        else:
            _ = dtb_entity_type.select()
        if _.exists():
            return _
        return []

    def find_all(self, entity_type, filters=None):
        return list(map(lambda x: self._to_entity(entity_type, x.__data__), self._find_all_fnc(entity_type, filters)))

    def find_all_iter(self, entity_type, filters=None):
        for x in self._find_all_fnc(entity_type, filters):
            yield self._to_entity(entity_type, x.__data__)

    # noinspection PyUnusedLocal
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
        dtb_entity_type = self._to_dtb_entity_type(entity_type)

        conditions = {
            #
            'today': '(dtb_entity_type.ctime >= today) & (dtb_entity_type.ctime < today+datetime.timedelta(days=1))',
            # yesterday <= ctime < today
            'yesterday': '(dtb_entity_type.ctime >= yesterday) & (dtb_entity_type.ctime < today)',
            # start_of_week <= ctime < yesterday
            'earlier_this_week': '(dtb_entity_type.ctime >= start_of_week) & (dtb_entity_type.ctime < yesterday)',
            #
            'last_week': '(dtb_entity_type.ctime >= start_of_last_week) & (dtb_entity_type.ctime < end_of_last_week)',
            'earlier_this_month': '(dtb_entity_type.ctime >= start_of_month) & (dtb_entity_type.ctime < start_of_last_week)',
            'last_month': '(dtb_entity_type.ctime >= start_of_last_month) & (dtb_entity_type.ctime < start_of_month)',
            'earlier_this_year': '(dtb_entity_type.ctime >= start_of_year) & (dtb_entity_type.ctime < start_of_last_month)',
            'long_time_ago': '(dtb_entity_type.ctime < start_of_year)'
        }
        if filters:
            _ = dtb_entity_type.select().where(
                eval(conditions[tag]+'&'+self._to_expression_str(entity_type, filters))
            )
        else:
            _ = dtb_entity_type.select().where(
                eval(conditions[tag])
            )
        if _.exists():
            return list(map(lambda x: self._to_entity(entity_type, x.__data__), _))
        return []

    def entity_is_exists(self, entity_type, path):
        dtb_entity_type = self._to_dtb_entity_type(entity_type)
        return dtb_entity_type.select().where(dtb_entity_type.path == path).exists()

    def get_entity(self, entity_type, path):
        dtb_entity_type = self._to_dtb_entity_type(entity_type)
        _ = dtb_entity_type.select().where(dtb_entity_type.path == path)
        if _.exists():
            return self._to_entity(entity_type, _.first().__data__)

    def get_entity_index_maximum(self, entity_type):
        dtb_entity_type = self._to_dtb_entity_type(entity_type)
        return dtb_entity_type.select(peewee.fn.MAX(dtb_entity_type.id)).scalar()

    def create_entity(self, entity_type, path, **kwargs):
        dtb_entity_type = self._to_dtb_entity_type(entity_type)
        if dtb_entity_type.select().where(dtb_entity_type.path == path).exists() is True:
            return self.get_entity(entity_type, path)

        dtb_entity_type = self._to_dtb_entity_type(entity_type)
        name = path.split(self.PATHSEP)[-1]
        names = bsc_pinyin.Text.split_any_to_words(name)
        gui_name = ' '.join(map(lambda x: str(x).capitalize(), names))
        gui_name_chs = gui_name
        options = dict(
            path=path,
            gui_name=gui_name,
            gui_name_chs=gui_name_chs
        )
        options.update(**kwargs)
        with Stage.LOCK:
            _ = dtb_entity_type.create(**options)
            _.save()
            return self._to_entity(entity_type, _.__data__)

    def remove_entity(self, entity_type, path):
        dtb_entity_type = self._to_dtb_entity_type(entity_type)
        if dtb_entity_type.select().where(dtb_entity_type.path == path).exists() is False:
            return False

        _ = dtb_entity_type.get(dtb_entity_type.path == path)
        _.delete_instance()
        return True

    def update_entity(self, entity_type, path, **kwargs):
        dtb_entity_type = self._to_dtb_entity_type(entity_type)
        _ = dtb_entity_type.select().where(dtb_entity_type.path == path)
        if _.exists():
            csr = _.first()
            for k, v in kwargs.items():
                if isinstance(v, six.string_types):
                    v = six.u('"""{}"""').format(v.replace(r'"', r'\"'))
                elif isinstance(v, bool):
                    v = v
                else:
                    v = json.dumps(v)
                exec (six.u(r'csr.{} = {}').format(k, v))
            csr.save()
            return True
        return False

    # type
    def create_type_as_group(self, path, **kwargs):
        options = dict(
            path=path, category='group', type='group', gui_icon_name='database/group'
        )
        options.update(**kwargs)
        return self.create_entity(
            self.EntityTypes.Type, **options
        )

    def create_type(self, path, **kwargs):
        options = dict(
            path=path, category='node', type='node', gui_icon_name='database/type'
        )
        options.update(**kwargs)
        return self.create_entity(
            self.EntityTypes.Type, **options
        )

    def get_type(self, path):
        return self.get_entity(
            self.EntityTypes.Type, path
        )

    def update_type(self, path, **kwargs):
        return self.update_entity(
            self.EntityTypes.Type, path, **kwargs
        )

    # tag
    def create_tag_as_group(self, path, **kwargs):
        options = dict(
            path=path, category='group', type='group', gui_icon_name='database/group'
        )
        options.update(**kwargs)
        return self.create_entity(
            self.EntityTypes.Tag, **options
        )

    def create_tag(self, path, **kwargs):
        options = dict(
            path=path, category='node', type='node', gui_icon_name='database/tag'
        )
        options.update(**kwargs)
        return self.create_entity(
            self.EntityTypes.Tag, **options
        )

    def get_tag(self, path):
        return self.get_entity(
            self.EntityTypes.Tag, path
        )

    def update_tag(self, path, **kwargs):
        return self.update_entity(
            self.EntityTypes.Tag, path, **kwargs
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

    def remove_assign(self, path_source, path_target):
        path = '{}->{}'.format(path_source, path_target)
        self.remove_entity(
            self.EntityTypes.Assign, path
        )

    def remove_assigns_below(self, path_source, path_target_root):
        if not path_target_root.endswith('/'):
            path_target_root += '/'
        path = '{}->{}'.format(path_source, path_target_root)
        _ = self.find_all(
            self.EntityTypes.Assign,
            filters=[
                ('path', 'startswith', path)
            ]
        )
        for i in _:
            self.remove_entity(
                self.EntityTypes.Assign, i.path
            )

    # node
    def create_node_type_assign(self, node_path, type_path, **kwargs):
        return self.create_assign(
            node_path, type_path, type=self.AssignTypes.Type, **kwargs
        )

    def remove_node_type_assign(self, node_path, type_path):
        self.remove_assign(node_path, type_path)

    def find_node_assign_types(self, node_path):
        _ = self.find_all(
            self.EntityTypes.Assign,
            filters=[
                ('source', 'is', node_path),
                ('type', 'is', self.AssignTypes.Type)
            ]
        )
        return list(filter(None, [self.get_type(x.target) for x in _]))

    def find_nodes_assign_type_path_set(self, node_paths):
        path_set = set()
        for i_node_path in node_paths:
            i_assigns = self.find_all(
                self.EntityTypes.Assign,
                filters=[
                    ('source', 'is', i_node_path),
                    ('type', 'is', self.AssignTypes.Type)
                ]
            )
            path_set.update(set([j.target for j in i_assigns]))
        return path_set

    def create_node_tag_assign(self, node_path, tag_path, **kwargs):
        return self.create_assign(
            node_path, tag_path, type=self.AssignTypes.Tag, **kwargs
        )

    def remove_node_tag_assign(self, node_path, tag_path):
        self.remove_assign(node_path, tag_path)

    def find_node_assign_tags(self, node_path):
        _ = self.find_all(
            self.EntityTypes.Assign,
            filters=[
                ('source', 'is', node_path),
                ('type', 'is', self.AssignTypes.Tag)
            ]
        )
        return list(filter(None, [self.get_tag(x.target) for x in _]))

    def find_nodes_assign_tag_path_set(self, node_paths):
        path_set = set()
        for i_node_path in node_paths:
            i_assigns = self.find_all(
                self.EntityTypes.Assign,
                filters=[
                    ('source', 'is', i_node_path),
                    ('type', 'is', self.AssignTypes.Tag)
                ]
            )
            path_set.update(set([j.target for j in i_assigns]))
        return path_set

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
        return self.update_entity(
            self.EntityTypes.Property, path, value=value, **kwargs
        )

    def create_or_update_node_property(self, node_path, port, value, **kwargs):
        path = '{}.{}'.format(node_path, port)
        if self.entity_is_exists(self.EntityTypes.Property, path) is False:
            return self.create_property(
                node_path, port, value, **kwargs
            )
        return self.update_property(
            node_path, port, value, **kwargs
        )

    def create_parameter(self, node_path, port, value, **kwargs):
        return self.create_property(node_path, port, value, type='parameter', **kwargs)

    def create_or_update_node_parameter(self, node_path, port, value, **kwargs):
        return self.create_or_update_node_property(node_path, port, value, type='parameter', **kwargs)

    # lock
    def set_node_locked(self, node_path, boolean):
        scr_entity = self.get_node(node_path)
        if not scr_entity:
            return False

        boolean = bool(boolean)
        if boolean == scr_entity.lock:
            return False

        self.update_node(node_path, lock=boolean)

        tag = ['unlock', 'lock'][boolean]

        value = self.get_node_parameter(node_path, 'lock_history')
        if value:
            _ = json.loads(value)
            # trim to 10
            history = _[-10:]
            history.append(
                [tag, bsc_core.BscSystem.get_user_name(), bsc_core.BscSystem.generate_timestamp()]
            )
        else:
            history = [
                [tag, bsc_core.BscSystem.get_user_name(), bsc_core.BscSystem.generate_timestamp()]
            ]

        self.create_or_update_node_parameter(node_path, 'lock_history', json.dumps(history))

        self.set_node_assigns_locked(node_path, boolean)
        return True

    # trash
    def set_node_trashed(self, entity_path, boolean):
        scr_entity = self.get_node(entity_path)
        if not scr_entity:
            return False

        boolean = bool(boolean)
        if boolean == scr_entity.trash:
            return False

        self.update_node(entity_path, trash=boolean)

        tag = ['recover', 'trash'][boolean]

        value = self.get_node_parameter(entity_path, 'trash_history')
        if value:
            _ = json.loads(value)
            # trim to 10
            history = _[-10:]
            history.append(
                [tag, bsc_core.BscSystem.get_user_name(), bsc_core.BscSystem.generate_timestamp()]
            )
        else:
            history = [
                [tag, bsc_core.BscSystem.get_user_name(), bsc_core.BscSystem.generate_timestamp()]
            ]

        self.create_or_update_node_parameter(entity_path, 'trash_history', json.dumps(history))

        self.set_node_assigns_trashed(entity_path, boolean)
        return True

    def set_type_trashed(self, entity_path, boolean):
        scr_entity = self.get_type(entity_path)
        if not scr_entity:
            return False

        boolean = bool(boolean)
        if boolean == scr_entity.trash:
            return False

        self.update_type(entity_path, trash=boolean)
        descendants = self.find_all(
            entity_type=self.EntityTypes.Type,
            filters=[
                ('path', 'startswith', '{}/'.format(entity_path))
            ]
        )
        if descendants:
            for i in descendants:
                self.update_type(i.path, trash=boolean)
        return True

    def set_tag_trashed(self, entity_path, boolean):
        scr_entity = self.get_tag(entity_path)
        if not scr_entity:
            return False

        boolean = bool(boolean)
        if boolean == scr_entity.trash:
            return False

        self.update_tag(entity_path, trash=boolean)
        descendants = self.find_all(
            entity_type=self.EntityTypes.Tag,
            filters=[
                ('path', 'startswith', '{}/'.format(entity_path))
            ]
        )
        if descendants:
            for i in descendants:
                self.update_tag(i.path, trash=boolean)
        return True

    def get_node_type_assigns(self, node_path):
        return self.find_all(
            self.EntityTypes.Assign,
            filters=[
                ('source', 'is', node_path),
                ('type', 'is', self.AssignTypes.Type)
            ]
        )

    def get_node_tag_assigns(self, node_path):
        return self.find_all(
            self.EntityTypes.Assign,
            filters=[
                ('source', 'is', node_path),
                ('type', 'is', self.AssignTypes.Tag)
            ]
        )

    def set_node_assigns_locked(self, node_path, boolean):
        """
        when node is locked, must lock type assign and tag assign
        """
        # lock type assigns
        type_assigns = self.get_node_type_assigns(node_path)
        for i_type_assign in type_assigns:
            self.update_entity(i_type_assign.entity_type, i_type_assign.path, lock=boolean)

        # lock tag assigns
        tag_assigns = self.get_node_tag_assigns(node_path)
        for i_tag_assign in tag_assigns:
            self.update_entity(i_tag_assign.entity_type, i_tag_assign.path, lock=boolean)

    def set_node_assigns_trashed(self, node_path, boolean):
        """
        when node is trashed, must trash type assign and tag assign
        """
        # trash type assigns
        type_assigns = self.get_node_type_assigns(node_path)
        for i_type_assign in type_assigns:
            self.update_entity(i_type_assign.entity_type, i_type_assign.path, trash=boolean)

        # trash tag assigns
        tag_assigns = self.get_node_tag_assigns(node_path)
        for i_tag_assign in tag_assigns:
            self.update_entity(i_tag_assign.entity_type, i_tag_assign.path, trash=boolean)

    def generate_node_lock_history(self, node_path, language):
        value = self.get_node_parameter(node_path, 'lock_history')
        if value:
            tag_dict = dict(
                lock='Locked',
                unlock='Unlocked'
            )
            tag_dict_chs = dict(
                lock='锁定了',
                unlock='解锁了'
            )
            texts = []
            _ = json.loads(value)
            for i in _:
                i_tag, i_user_name, i_timestamp = i
                if language == 'chs':
                    texts.append(
                        u'{}被"{}"{}；'.format(
                            bsc_core.BscTimePrettify.to_prettify_by_timestamp(i_timestamp, language=0),
                            i_user_name,
                            bsc_core.ensure_unicode(tag_dict_chs[i_tag])
                        )
                    )
                else:
                    texts.append(
                        '{} by "{}" at {};'.format(
                            tag_dict[i_tag],
                            i_user_name,
                            bsc_core.BscTimePrettify.to_prettify_by_timestamp(i_timestamp, language=1)
                        )
                    )
            return '\n'.join(texts)
        return ''

    def upload_node_preview(self, node_path, file_path):
        if self.node_is_exists(node_path) is False:
            return False

        file_opt = bsc_storage.StgFileOpt(file_path)
        if file_opt.get_is_file() is False:
            return False

        node_name = bsc_core.BscNodePathOpt(node_path).name
        options = copy.copy(self._options)
        options['node'] = node_name
        # use jpg default
        thumbnail_jpg_path = self.NodePathPattens.ThumbnailJpg.format(**options)
        options['format'] = file_opt.format
        # image
        if file_opt.ext in {'.png', '.jpg', '.tga', '.exr'}:
            jpg_path = self.NodePathPattens.PreviewJpg.format(**options)
            bsc_storage.ImgOiioOpt(file_path).create_compress(jpg_path, replace=True)
            # noinspection PyBroadException
            try:
                # fixme: convert png to jpg?
                bsc_storage.ImgOiioOpt(jpg_path).create_compress(thumbnail_jpg_path, replace=True)
                self.create_or_update_node_parameter(
                    node_path, 'image', jpg_path
                )
                self.create_or_update_node_parameter(
                    node_path, 'thumbnail', thumbnail_jpg_path
                )
                return True
            except Exception:
                bsc_core.Debug.trace()
                return False
        # video
        elif file_opt.ext in {'.mov', '.avi', '.mp4'}:
            mov_path = self.NodePathPattens.PreviewMov.format(**options)
            bsc_core.BscFfmpegVideo.create_compress(file_path, mov_path, replace=True)
            # noinspection PyBroadException
            try:
                self.create_or_update_node_parameter(
                    node_path, 'video', mov_path
                )
                bsc_core.BscFfmpegVideo.extract_frame(mov_path, thumbnail_jpg_path, 0)
                self.create_or_update_node_parameter(
                    node_path, 'thumbnail', thumbnail_jpg_path
                )
                thumbnail_sequence_path = bsc_core.BscFfmpegVideo.extract_all_frames(
                    mov_path,
                    image_format=self.DEFAULT_THUMBNAIL_FORMAT,
                    width_maximum=self.DEFAULT_THUMBNAIL_WIDTH_MAXIMUM
                )
                self.create_or_update_node_parameter(
                    node_path, 'thumbnail_sequence', thumbnail_sequence_path
                )
                return True
            except Exception:
                bsc_core.Debug.trace()
                return False

        return False

    def upload_node_thumbnail(self, node_path, file_path):
        pass

    def upload_node_preview_as_image_sequence(self, node_path, file_path):
        if self.node_is_exists(node_path) is False:
            return False

        if bsc_storage.StgFileTiles.get_is_exists(file_path) is False:
            return False

        node_name = bsc_core.BscNodePathOpt(node_path).name
        options = copy.copy(self._options)
        options['node'] = node_name
        file_opt = bsc_storage.StgFileOpt(file_path)
        options['format'] = file_opt.format

        image_sequence_path = self.NodePathPattens.PreviewImageSequence.format(**options)
        thumbnail_jpg_path = self.NodePathPattens.ThumbnailJpg.format(**options)

        file_paths = bsc_storage.StgFileTiles.get_tiles(file_path)
        file_paths.sort()
        for i_seq, i_file_path in enumerate(file_paths):
            i_file_path_dst = image_sequence_path.replace('%04d', str(i_seq).zfill(4))
            bsc_storage.StgFileOpt(i_file_path).copy_to_file(i_file_path_dst)

        # copy first frame as thumbnail
        bsc_storage.StgFileOpt(file_paths[0]).copy_to_file(thumbnail_jpg_path)

        self.create_or_update_node_parameter(
            node_path, 'image_sequence', image_sequence_path
        )
        self.create_or_update_node_parameter(
            node_path, 'thumbnail', thumbnail_jpg_path
        )

    def upload_node_audio(self, node_path, file_path, collect_source=False):
        file_opt = bsc_storage.StgFileOpt(file_path)
        if file_opt.get_is_file() is False:
            return False

        node_name = bsc_core.BscNodePathOpt(node_path).name
        options = copy.copy(self._options)
        options['node'] = node_name

        thumbnail_jpg_path = self.NodePathPattens.ThumbnailJpg.format(**options)

        import lxbasic.cv.core as bsc_cv_core

        capture_opt = bsc_cv_core.AudioCaptureOpt(file_path)
        capture_opt.create_thumbnail(thumbnail_jpg_path, replace=False)

        preview_audio_mp3_path = self.NodePathPattens.PreviewMp3.format(**options)
        capture_opt.create_compress(preview_audio_mp3_path, replace=False)

        self.create_or_update_node_parameter(
            node_path, 'thumbnail', thumbnail_jpg_path
        )

        self.create_or_update_node_parameter(
            node_path, 'source_type', 'audio'
        )

        self.create_or_update_node_parameter(
            node_path, 'audio', preview_audio_mp3_path
        )

        if collect_source is True:
            source_dir_path = self.generate_node_source_dir_path(node_path)
            file_path = file_opt.copy_to_directory(source_dir_path)

        self.create_or_update_node_parameter(
            node_path, 'source', file_path
        )

    def upload_node_video(self, node_path, file_path, collect_source=False):
        file_opt = bsc_storage.StgFileOpt(file_path)
        if file_opt.get_is_file() is False:
            return False

        node_name = bsc_core.BscNodePathOpt(node_path).name
        options = copy.copy(self._options)
        options['node'] = node_name

        thumbnail_jpg_path = self.NodePathPattens.ThumbnailJpg.format(**options)

        import lxbasic.cv.core as bsc_cv_core
        bsc_cv_core.VideoCaptureOpt(file_path).create_thumbnail(thumbnail_jpg_path, replace=True)

        preview_video_path = self.NodePathPattens.PreviewMov.format(**options)

        bsc_core.BscFfmpegVideo.create_compress(file_path, preview_video_path, replace=False)

        self.create_or_update_node_parameter(
            node_path, 'thumbnail', thumbnail_jpg_path
        )

        self.create_or_update_node_parameter(
            node_path, 'source_type', 'video'
        )

        self.create_or_update_node_parameter(
            node_path, 'video', preview_video_path
        )

        if collect_source is True:
            source_dir_path = self.generate_node_source_dir_path(node_path)
            file_path = file_opt.copy_to_directory(source_dir_path)

        self.create_or_update_node_parameter(
            node_path, 'source', file_path
        )

    def upload_node_preview_as_image(self, node_path, file_path):
        pass

    def upload_node_json(self, node_path, tag, data):
        if self.node_is_exists(node_path) is False:
            return False

        node_name = bsc_core.BscNodePathOpt(node_path).name
        options = copy.copy(self._options)
        options['node'] = node_name
        options['tag'] = tag

        json_path = self.NodePathPattens.Json.format(**options)

        json_opt = bsc_storage.StgFileOpt(json_path)
        json_opt.set_write(data)

        self.create_or_update_node_parameter(
            node_path, tag, json_path
        )

    def generate_node_json_path(self, node_path, tag):
        node_name = bsc_core.BscNodePathOpt(node_path).name
        options = copy.copy(self._options)
        options['node'] = node_name
        options['tag'] = tag

        return self.NodePathPattens.Json.format(**options)

    def upload_node_maya_scene(self, node_path, tag, file_path):
        maya_scene_path = self.generate_node_maya_scene_path(node_path, tag)
        file_opt = bsc_storage.StgFileOpt(file_path)
        file_opt.copy_to_file(maya_scene_path)
        self.create_or_update_node_parameter(
            node_path, tag, maya_scene_path
        )

    def generate_node_maya_scene_path(self, node_path, tag):
        node_name = bsc_core.BscNodePathOpt(node_path).name
        options = copy.copy(self._options)
        options['node'] = node_name
        options['tag'] = tag
        return self.NodePathPattens.MayaScene.format(**options)

    def generate_node_motion_json_path(self, node_path, tag):
        options = copy.copy(self._options)
        options['node'] = bsc_core.BscNodePathOpt(node_path).name
        options['tag'] = tag
        return self.NodePathPattens.Json.format(**options)

    def generate_node_base_dir_path(self, node_path):
        options = copy.copy(self._options)
        options['node'] = bsc_core.BscNodePathOpt(node_path).name
        return self.NodePathPattens.BaseDir.format(**options)

    def generate_node_source_dir_path(self, node_path):
        options = copy.copy(self._options)
        options['node'] = bsc_core.BscNodePathOpt(node_path).name
        return self.NodePathPattens.SourceDir.format(**options)

    def generate_node_preview_mov_path(self, node_path):
        options = copy.copy(self._options)
        options['node'] = bsc_core.BscNodePathOpt(node_path).name
        return self.NodePathPattens.PreviewMov.format(**options)

    def generate_node_image_sequence_dir_path(self, node_path):
        options = copy.copy(self._options)
        options['node'] = bsc_core.BscNodePathOpt(node_path).name
        return self.NodePathPattens.PreviewImageDir.format(**options)

    def get_node(self, path):
        return self.get_entity(
            self.EntityTypes.Node, path
        )

    def update_node(self, path, **kwargs):
        return self.update_entity(
            self.EntityTypes.Node, path, **kwargs
        )

    def get_node_parameter(self, node_path, port):
        path = '{}.{}'.format(node_path, port)
        p = self.get_entity(
            self.EntityTypes.Property, path
        )
        if p:
            return p.value

    def get_node_parameter_as_boolean(self, node_path, port):
        value = self.get_node_parameter(node_path, port)
        if value is not None:
            if str(value).isdigit():
                return not not eval(value)
            else:
                if value.lower() == 'true':
                    return True
        return False

    def is_exists_node_tag(self, node_path, tag_path):
        path = '{}->{}'.format(node_path, tag_path)
        _ = self.find_one(
            self.EntityTypes.Assign,
            filters=[
                ('path', 'is', path)
            ]
        )
        if _:
            return True
        return False

    def node_is_exists(self, path):
        return self.entity_is_exists(self.EntityTypes.Node, path)

    def copy_from(self, stage):
        entity_types = self.EntityTypes.All
        with bsc_log.LogProcessContext.create(
            maximum=len(entity_types), label='copy entity type'
        ) as l_p_0:

            for i_entity_type in entity_types:
                i_entities = stage.find_all(i_entity_type)
                with bsc_log.LogProcessContext.create(
                    maximum=len(i_entities), label='copy entity',
                ) as l_p_1:
                    for j_entity in i_entities:
                        j_entity_options = dict()
                        j_entity_options.update(j_entity)
                        self.create_entity(i_entity_type, **j_entity_options)

                        l_p_1.do_update()

                l_p_0.do_update()
