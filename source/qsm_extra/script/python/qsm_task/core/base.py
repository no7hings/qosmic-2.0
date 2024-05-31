# coding:utf-8
import os

import time

import datetime

import uuid

import getpass

import socket

import lxbasic.content as bsc_content


class Util(object):
    CONNECTION = None

    DATE_TAG_FORMAT = '%Y_%m%d'

    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def get_host_name(cls):
        return socket.gethostname()

    @classmethod
    def get_user_name(cls):
        return getpass.getuser()
    
    @classmethod
    def get_date_tag(cls):
        timestamp = time.time()
        return time.strftime(
            cls.DATE_TAG_FORMAT,
            time.localtime(timestamp)
        )

    @classmethod
    def new_uuid(cls):
        return str(uuid.uuid1()).upper()

    @classmethod
    def get_utc_time(cls):
        utc_now = datetime.datetime.utcnow()
        return utc_now.strftime(
            cls.TIME_FORMAT
        )

    @classmethod
    def get_time(cls):
        return time.strftime(
            cls.TIME_FORMAT,
            time.localtime(time.time())
        )


class TaskProperties(dict):
    class Keys(object):
        ID = 'id'
        Name = 'name'
        Time = 'time'
        UtcTime = 'utc_time'

        HostName = 'host_name'
        UserName = 'user_name'

        Priority = 'priority'

        SubmitTime = 'submit_time'
        StartTime = 'start_time'
        FinishTime = 'finish_time'

        All = [
            ID, Name,
            HostName, UserName,
            Priority,
            # SubmitTime, StartTime, FinishTime
        ]

    def __init__(self, *args, **kwargs):
        super(TaskProperties, self).__init__(*args, **kwargs)

    def __getattr__(self, key):
        return self.__getitem__(key)


class AbsEntity(object):

    def __init__(self, entities_cache, entity_id):
        self._entities_cache = entities_cache
        self._entity_id = entity_id
        self._location = '{}/{}.entity'.format(
            self._entities_cache.location, self._entity_id
        )
        self._json_location = '{}/entity.json'.format(
            self._location
        )
        self._json_content = bsc_content.Content(
            key=None, value=self._json_location
        )

    def __str__(self):
        return '{}(id="{}")'.format(
            self.__class__.__name__,
            self._entity_id
        )

    def __repr__(self):
        return self.__str__()

    @property
    def id(self):
        return self._entity_id

    @property
    def location(self):
        return self._location

    @property
    def content(self):
        return self._json_content

    @classmethod
    def create(cls, entities_cache, entity_id, entity_index, **kwargs):
        location = '{}/{}.entity'.format(
            entities_cache.location, entity_id
        )
        json_location = '{}/entity.json'.format(
            location
        )
        if os.path.isfile(json_location) is False:
            properties = dict(
                id=entity_id,
                index=entity_index,
                #
                time=Util.get_time(),
                utc_time=Util.get_utc_time(),
                #
                host=Util.get_host_name(),
                user=Util.get_user_name(),
            )
            properties.update(**kwargs)
            bsc_content.ContentFile(
                json_location
            ).write(
                {
                    'properties': properties,
                }

            )
        return cls(entities_cache, entity_id)

    def do_update(self):
        pre_hash_key = self._json_content.__hash__()
        self._json_content.reload()
        hash_key = self._json_content.__hash__()
        if pre_hash_key != hash_key:
            return True
        return False

    def get_properties(self):
        return self._json_content.get('properties')

    def set(self, key, value):
        self._json_content.set(
            key, value
        )

    def get(self, key):
        return self._json_content.get(
            'properties.{}'.format(key)
        )


class AbsEntityPool(object):
    LOCATION_PTN = None

    CACHE = None

    CACHE_CLS = None

    @classmethod
    def generate(cls):
        if cls.CACHE is not None:
            return cls.CACHE
        _ = cls(
            cls.LOCATION_PTN.format(
                user_name=Util.get_user_name()
            )
        )
        cls.CACHE = _
        return _

    def __init__(self, location):
        self._location = location
        self._cache = self.CACHE_CLS(self)

    def __str__(self):
        return '{}(location="{}")'.format(
            self.__class__.__name__, self._location
        )

    def __repr__(self):
        return self.__str__()

    @property
    def location(self):
        return self._location

    def do_update(self):
        return self._cache.do_update()

    def get_entity_ids(self):
        return self._cache.get_entity_ids()

    def find_entity_ids(self, **kwargs):
        return self._cache.find_entity_ids(**kwargs)

    def find_entities(self, entity_ids):
        return self._cache.find_entities(entity_ids)

    def get_entities(self):
        return self._cache.get_entities()

    def find_entity(self, entity_id):
        return self._cache.find_entity(entity_id)

    def new_entity(self, **kwargs):
        return self._cache.new_entity(**kwargs)

    def send_entity_to_trash(self, entity_id):
        return self._cache.send_entity_to_trash(entity_id)

    def update_entity_status(self, entity_id, status):
        pass


class AbsEntitiesCache(object):
    ENTITY_CLS = None

    def __init__(self, entity_pool):
        self._entity_pool = entity_pool

        self._location = '{}/entities'.format(
            self._entity_pool.location
        )
        self._json_location = '{}/entities.json'.format(
            self._location
        )
        if os.path.isfile(self._json_location) is False:
            bsc_content.ContentFile(
                self._json_location
            ).write(
                dict(
                    properties=dict(
                        utc_time=Util.get_utc_time(),
                        time=Util.get_time(),
                    ),
                    entities=dict()
                )
            )

        self._json_content = bsc_content.Content(
            key=None, value=self._json_location
        )

        self._entity_dict = {}
        self._entity_index_dict = {}
        self._entity_ids_new = []

    def __str__(self):
        return '{}(location="{}")'.format(
            self.__class__.__name__, self._location
        )

    def __repr__(self):
        return self.__str__()

    @property
    def location(self):
        return self._location

    @property
    def content(self):
        return self._json_content

    def do_update(self):
        # reload json
        self._json_content.reload()

        self._entity_ids_new = []
        for i_entity_id in self.get_entity_ids():
            if i_entity_id not in self._entity_dict:
                i_entity = self.ENTITY_CLS(self, i_entity_id)
                self.register_entity_cache(i_entity_id, i_entity)
                self._entity_ids_new.append(i_entity_id)
        return self._entity_ids_new

    def register_entity_cache(self, entity_id, entity):
        index = self.get_entity_index(entity_id)
        self._entity_index_dict[entity_id] = index
        self._entity_dict[entity_id] = entity

    def get_entity_ids(self):
        return self._json_content.get_key_names_at('entities')

    def find_entity_ids(self, **kwargs):
        if 'ignore_delete' in kwargs:
            if kwargs['ignore_delete'] is True:
                _ = self._json_content.get_key_names_at('entities')
                return [x for x in _ if self.get_entity_delete_flag(x) is False]
        return self._json_content.get_key_names_at('entities')

    def get_entity_index(self, entity_id):
        return self._json_content.get(
            'entities.{}.index'.format(entity_id)
        )

    def is_entity_valid(self, entity_id):
        return self._json_content.get_key_is_exists(
            'entities.{}'.format(entity_id)
        )

    def is_entity_exists(self, entity_id):
        return entity_id in self._entity_dict

    def find_entity(self, entity_id):
        if entity_id in self._entity_dict:
            return self._entity_dict[entity_id]

        if self.is_entity_valid(entity_id):
            entity = self.ENTITY_CLS(self, entity_id)
            self.register_entity_cache(entity_id, entity)
            return entity

    def find_entities(self, entity_ids):
        return [self.find_entity(x) for x in entity_ids]

    def get_entities(self):
        _ = self._entity_dict.values()
        _.sort(key=lambda x: self._entity_index_dict[x.id])
        return _

    def new_entity(self, **kwargs):
        entity_id = Util.new_uuid()

        entity_index = len(self.get_entity_ids())
        entity = self.ENTITY_CLS.create(self, entity_id, entity_index, **kwargs)
        self._json_content.set(
            'entities.{}'.format(entity_id),
            dict(
                index=entity_index,
                time=Util.get_time(),
                utc_time=Util.get_utc_time(),
            )
        )
        # save first
        self.accept()
        self.register_entity_cache(entity_id, entity)
        return entity

    def send_entity_to_trash(self, entity_id):
        if entity_id in self._entity_dict:
            self._json_content.set(
                'entities.{}.delete_flag'.format(entity_id), True
            )
            self.accept()

    def send_entities_to_trash(self, entity_ids):
        for i_entity_id in entity_ids:
            if i_entity_id in self._entity_dict:
                self._json_content.set(
                    'entities.{}.delete_flag'.format(i_entity_id), True
                )

        self.accept()

    def get_entity_delete_flag(self, entity_id):
        if self.is_entity_valid(entity_id):
            return self._json_content.get(
                'entities.{}.delete_flag'.format(entity_id), False
            )
        return False

    def accept(self):
        self._json_content.save()
    
