# coding:utf-8
import _base


class AbsBase(object):
    VERBOSE_LEVEL = 1


class AbsEntity(AbsBase):
    EntityType = None
    VariantKey = None
    ENTITY_PATH_PTN = None

    @classmethod
    def _generate_variants_fnc(cls, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    def _generate_path_fnc(cls, *args, **kwargs):
        return cls._path_fnc(cls._generate_variants_fnc(*args, **kwargs))

    @classmethod
    def _path_fnc(cls, variants):
        return cls.ENTITY_PATH_PTN.format(**variants)

    def __init__(self, stage, variants):
        self._stage = stage
        self._properties = _base.Properties(**variants)

        self._path = self._path_fnc(variants)
        self._name = self._properties[self.VariantKey]

    @property
    def stage(self):
        return self._stage

    @property
    def properties(self):
        return self._properties

    @property
    def type(self):
        return self.EntityType

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    def get_location(self):
        return self._stage.generate_location_for(
            '{}-dir'.format(self.VariantKey), self._properties
        )

    def __str__(self):
        return '{}(path={})'.format(
            self.__class__.__name__,
            self.path
        )
