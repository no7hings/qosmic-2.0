# coding:utf-8
import six

from ..core import base as _cor_base

from . import _base

from . import _role

from . import _asset

from . import _episode

from . import _sequence

from . import _shot

from . import _task

from . import _step


class Project(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Project
    VariantKey = _cor_base.EntityVariantKeys.Project

    NextEntitiesGeneratorClsDict = {
        _cor_base.EntityTypes.Role: _role.RolesGenerator,
        _cor_base.EntityTypes.Asset: _asset.AssetsGenerator,
        _cor_base.EntityTypes.Episode: _episode.EpisodesGenerator,
        _cor_base.EntityTypes.Sequence: _sequence.SequencesGenerator,
        _cor_base.EntityTypes.Shot: _shot.ShotsGenerator,
    }

    TasksGeneratorCls = _task.TasksGenerator

    @classmethod
    def _variant_validation_fnc(cls, variants):
        return _cor_base.EntityVariantKeyFnc.match_fnc(variants, cls.VariantKey)

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)

    def _new_step_fnc(self, variants):
        path = _cor_base.AbsEntityBase.to_step_path(variants)
        return _step.Step(self, path, variants)

    def _find_step_variants(self, **kwargs):
        list_ = []

        if 'resource_type' in kwargs:
            _ = kwargs['resource_type']
            if isinstance(_, six.string_types):
                resource_types = [_]
            elif isinstance(_, list):
                resource_types = _
            else:
                raise RuntimeError()
        else:
            resource_types = self.ResourceTypes.All

        for i in resource_types:
            i_step_names = _cor_base.DisorderConfig()._resource_step_dict.get(i, [])
            for j_step_name in i_step_names:
                list_.append(
                    dict(
                        project=self._variants['project'],
                        resource_type=kwargs['resource_type'],
                        step=j_step_name
                    )
                )
        return list_

    # step
    def steps(self, **kwargs):
        list_ = []
        for i in self._find_step_variants(**kwargs):
            i_step = self._new_step_fnc(i)
            list_.append(i_step)
        return list_

    def step(self, name, **kwargs):
        return None

    # role
    @_base.EntityFactory.find_all(_cor_base.EntityTypes.Role)
    def roles(self, **kwargs):
        pass

    @_base.EntityFactory.find_one(_cor_base.EntityTypes.Role)
    def role(self, name, **kwargs):
        pass

    # asset
    @_base.EntityFactory.find_all(_cor_base.EntityTypes.Asset)
    def assets(self, **kwargs):
        pass

    @_base.EntityFactory.find_one(_cor_base.EntityTypes.Asset)
    def asset(self, name, **kwargs):
        pass

    # episode
    @_base.EntityFactory.find_all(_cor_base.EntityTypes.Episode)
    def episodes(self, **kwargs):
        pass

    @_base.EntityFactory.find_one(_cor_base.EntityTypes.Episode)
    def episode(self, name, **kwargs):
        pass

    # sequence
    @_base.EntityFactory.find_all(_cor_base.EntityTypes.Sequence)
    def sequences(self, **kwargs):
        pass

    @_base.EntityFactory.find_one(_cor_base.EntityTypes.Sequence)
    def sequence(self, name, **kwargs):
        pass

    # shot
    @_base.EntityFactory.find_all(_cor_base.EntityTypes.Shot)
    def shots(self, **kwargs):
        pass

    @_base.EntityFactory.find_one(_cor_base.EntityTypes.Shot)
    def shot(self, name, **kwargs):
        pass


class ProjectsGenerator(_base.AbsEntitiesGenerator):
    EntityCls = Project

    def __init__(self, *args, **kwargs):
        super(ProjectsGenerator, self).__init__(*args, **kwargs)
