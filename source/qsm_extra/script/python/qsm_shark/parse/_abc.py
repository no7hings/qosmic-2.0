# coding:utf-8
import functools

import time

import six

import sys

import _base


class AbsBase(object):
    EntityTypes = _base.EntityTypes
    SpaceKeys = _base.SpaceKeys

    # 1 is error only
    VERBOSE_LEVEL = 1

    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

    @staticmethod
    def ensure_string(text):
        if isinstance(text, six.text_type):
            return text.encode('utf-8')
        return text

    @staticmethod
    def ensure_unicode(s):
        if isinstance(s, six.text_type):
            return s
        elif isinstance(s, bytes):
            return s.decode('utf-8')
        else:
            return s

    @classmethod
    def stdout(cls, text):
        if cls.VERBOSE_LEVEL < 1:
            text = cls.ensure_string(text)
            sys.stdout.write(
                '{}         | {}\n'.format(time.strftime(
                    cls.TIME_FORMAT, time.localtime(time.time())),
                    text
                ),
            )

    @classmethod
    def stderr(cls, text):
        if cls.VERBOSE_LEVEL <= 1:
            text = cls.ensure_string(text)
            sys.stderr.write(
                '{}         | {}\n'.format(time.strftime(
                    cls.TIME_FORMAT, time.localtime(time.time())),
                    text
                ),
            )

    @classmethod
    def shorten_text(cls, text, max_length=120, placeholder="..."):
        if len(text) <= max_length:
            return text
        keep_length = (max_length-len(placeholder))//2
        return text[:keep_length]+placeholder+text[-keep_length:]


class AbsEntity(AbsBase):

    def __init__(self, stage, entity_type, variants):
        self._stage = stage
        self._variants = _base.Properties(**variants)

        self._entity_type = entity_type
        self._variants['entity_type'] = self._entity_type
        self._entity_key = self._stage._to_entity_key(entity_type, variants)
        self._variants['entity_key'] = self._entity_key
        self._entity_path = self._stage._to_entity_path(entity_type, variants)
        self._variants['entity_path'] = self._entity_path

        if self.VERBOSE_LEVEL < 1:
            self.stdout('new {}: {}'.format(entity_type, self._entity_path))

        # register method from configure, etc. <Project>.assets(), <Project>.asset("sam")
        method_data = self._stage._get_entity_next_method_data(self._entity_type)
        for k, v in method_data.items():
            i_fnc_name = v['fnc_name']
            i_kwargs = v['kwargs']
            # convert to args, exception use kwargs
            i_args = i_kwargs.values()
            i_fnc_src = self.__getattribute__(i_fnc_name)
            i_fnc = functools.partial(i_fnc_src, *i_args)
            setattr(self, k, i_fnc)

    def __str__(self):
        return self.shorten_text(
            '{}({})'.format(
                self._entity_type, self.ensure_string(self._entity_key)
            )
        )

    def __repr__(self):
        return '\n'+self.__str__()

    @property
    def stage(self):
        return self._stage

    @property
    def variants(self):
        return self._variants

    @property
    def type(self):
        return self._entity_type

    @property
    def path(self):
        return self._entity_path

    def find_one(self, entity_type, name, **kwargs):
        return self._stage._find_entity(
            self, entity_type, name, **kwargs
        )

    def find_all(self, entity_type, **kwargs):
        return self._stage._find_entities(
            self, entity_type, **kwargs
        )