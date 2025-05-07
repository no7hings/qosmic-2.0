# coding:utf-8
import lxbasic.content as bsc_content

import lxbasic.resource as bsc_resource


class SsnHookEngine(object):
    CONTENT = None

    @classmethod
    def _generate_content(cls):
        if cls.CONTENT is not None:
            return cls.CONTENT
        cls.CONTENT = bsc_content.Content(
            value=bsc_resource.BscConfigure.get_yaml('session/hook-engine')
        )
        cls.CONTENT.do_flatten()
        return cls.CONTENT

    @classmethod
    def get_all(cls):
        c = cls._generate_content()
        return c.get_key_names_at('command') or []

    @classmethod
    def get_command(cls, hook_engine, **kwargs):
        c = cls._generate_content()
        _ = c.get(
            'command.{}'.format(hook_engine)
        )
        return _.format(**kwargs)
