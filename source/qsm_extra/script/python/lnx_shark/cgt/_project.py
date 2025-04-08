# coding:utf-8
import six

from ..core import base as _cor_base

from . import _base

from . import _role

from . import _asset

from . import _episode

from . import _sequence

from . import _shot


class Project(_base.AbsEntity):
    Type = _cor_base.EntityTypes.Project

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)

    # role
    def roles(self, **kwargs):
        t_tw = self._stage._tw

        list_ = []

        filters = []

        cgt_dtb = self._cgt_variants['project.database']
        cgt_type = 'asset_type'

        for i_cgt_variants in t_tw.info.get(
            cgt_dtb, cgt_type,
            t_tw.info.get_id(cgt_dtb, cgt_type, filters),
            t_tw.info.fields(cgt_dtb, cgt_type)
        ):
            list_.append(
                _role.Role(
                    self._root,
                    dict(
                        project=self._variants['project'],
                        role=i_cgt_variants['asset_type.entity'],
                    ),
                    i_cgt_variants
                )
            )
        return list_

    def role(self, name, **kwargs):
        t_tw = self._stage._tw

        filters = [['asset_type.entity', '=', name]]

        cgt_dtb = self._cgt_variants['project.database']
        cgt_type = 'asset_type'

        id_list = t_tw.info.get_id(cgt_dtb, cgt_type, filters)
        if id_list:
            cgt_variants = t_tw.info.get(
                cgt_dtb, cgt_type,
                id_list, t_tw.info.fields(cgt_dtb, cgt_type)
            )[0]
            return _role.Role(
                self._root,
                dict(
                    project=self._variants['project'],
                    role=cgt_variants['asset_type.entity'],
                ),
                cgt_variants
            )

    # asset
    def assets(self, **kwargs):
        """
        @param kwargs: role = str or list
        @return: list
        """
        t_tw = self._stage._tw

        list_ = []

        filters = []
        if 'role' in kwargs:
            vs = kwargs['role']
            if isinstance(vs, six.string_types):
                opt = '='
            elif isinstance(vs, list):
                opt = 'in'
            else:
                raise RuntimeError()
            filters.append(['asset_type.entity', opt, vs])

        cgt_dtb = self._cgt_variants['project.database']
        cgt_type = 'asset'

        for i_cgt_variants in t_tw.info.get(
            cgt_dtb, cgt_type,
            t_tw.info.get_id(cgt_dtb, cgt_type, filters),
            t_tw.info.fields(cgt_dtb, cgt_type)
        ):
            list_.append(
                _asset.Asset(
                    self._root,
                    dict(
                        project=self._variants['project'],
                        role=i_cgt_variants['asset_type.entity'],
                        asset=i_cgt_variants['asset.entity']
                    ),
                    i_cgt_variants
                )
            )
        return list_

    def asset(self, name, **kwargs):
        t_tw = self._stage._tw

        filters = [['asset.entity', '=', name]]

        cgt_dtb = self._cgt_variants['project.database']
        cgt_type = 'asset'

        id_list = t_tw.info.get_id(cgt_dtb, cgt_type, filters)
        if id_list:
            cgt_variants = t_tw.info.get(
                cgt_dtb, cgt_type,
                id_list, t_tw.info.fields(cgt_dtb, cgt_type)
            )[0]
            return _asset.Asset(
                self._root,
                dict(
                    project=self._variants['project'],
                    role=cgt_variants['asset_type.entity'],
                    asset=cgt_variants['asset.entity']
                ),
                cgt_variants
            )

    # episode
    def episodes(self, **kwargs):
        t_tw = self._stage._tw

        list_ = []

        filters = []

        cgt_dtb = self._cgt_variants['project.database']
        cgt_type = 'eps'

        for i_cgt_variants in t_tw.info.get(
            cgt_dtb, cgt_type,
            t_tw.info.get_id(cgt_dtb, cgt_type, filters),
            t_tw.info.fields(cgt_dtb, cgt_type)
        ):
            list_.append(
                _episode.Episode(
                    self._root,
                    dict(
                        project=self._variants['project'],
                        episode=i_cgt_variants['eps.entity'],
                    ),
                    i_cgt_variants
                )
            )
        return list_

    def episode(self, name, **kwargs):
        t_tw = self._stage._tw

        filters = [['eps.entity', '=', name]]

        cgt_dtb = self._cgt_variants['project.database']
        cgt_type = 'eps'

        id_list = t_tw.info.get_id(cgt_dtb, cgt_type, filters)
        if id_list:
            cgt_variants = t_tw.info.get(
                cgt_dtb, cgt_type,
                id_list, t_tw.info.fields(cgt_dtb, cgt_type)
            )[0]
            return _episode.Episode(
                self._root,
                dict(
                    project=self._variants['project'],
                    episode=cgt_variants.get('eps.entity'),
                ),
                cgt_variants
            )

    # sequence
    def sequences(self, **kwargs):
        t_tw = self._stage._tw

        list_ = []

        filters = []
        if 'episode' in kwargs:
            vs = kwargs['episode']
            if isinstance(vs, six.string_types):
                opt = '='
            elif isinstance(vs, list):
                opt = 'in'
            else:
                raise RuntimeError()
            filters.append(['eps.entity', opt, vs])

        cgt_dtb = self._cgt_variants['project.database']
        cgt_type = 'seq'

        for i_cgt_variants in t_tw.info.get(
            cgt_dtb, cgt_type,
            t_tw.info.get_id(cgt_dtb, cgt_type, filters),
            t_tw.info.fields(cgt_dtb, cgt_type)
        ):
            list_.append(
                _sequence.Sequence(
                    self._root,
                    dict(
                        project=self._variants['project'],
                        episode=i_cgt_variants['eps.entity'],
                        sequence=i_cgt_variants['seq.entity']
                    ),
                    i_cgt_variants
                )
            )
        return list_

    def sequence(self, name, **kwargs):
        t_tw = self._stage._tw

        filters = [['seq.entity', '=', name]]

        cgt_dtb = self._cgt_variants['project.database']
        cgt_type = 'seq'

        id_list = t_tw.info.get_id(cgt_dtb, cgt_type, filters)
        if id_list:
            cgt_variants = t_tw.info.get(
                cgt_dtb, cgt_type,
                id_list, t_tw.info.fields(cgt_dtb, cgt_type)
            )[0]
            return _sequence.Sequence(
                self._root,
                dict(
                    project=self._variants['project'],
                    episode=cgt_variants.get('eps.entity'),
                    sequence=cgt_variants.get('seq.entity')
                ),
                cgt_variants
            )

    # shot
    def shots(self, **kwargs):
        t_tw = self._stage._tw

        list_ = []

        filters = []
        if 'episode' in kwargs:
            vs = kwargs['episode']
            if isinstance(vs, six.string_types):
                opt = '='
            elif isinstance(vs, list):
                opt = 'in'
            else:
                raise RuntimeError()
            filters.append(['eps.entity', opt, vs])
        if 'sequence' in kwargs:
            vs = kwargs['sequence']
            if isinstance(vs, six.string_types):
                opt = '='
            elif isinstance(vs, list):
                opt = 'in'
            else:
                raise RuntimeError()
            filters.append(['seq.entity', opt, vs])

        cgt_dtb = self._cgt_variants['project.database']
        cgt_type = 'shot'

        for i_cgt_variants in t_tw.info.get(
            cgt_dtb, cgt_type,
            t_tw.info.get_id(cgt_dtb, cgt_type, filters),
            t_tw.info.fields(cgt_dtb, cgt_type)
        ):
            list_.append(
                _shot.Shot(
                    self._root,
                    dict(
                        project=self._variants['project'],
                        # may no episode?
                        episode=i_cgt_variants.get('eps.entity'),
                        sequence=i_cgt_variants.get('seq.entity'),
                        shot=i_cgt_variants['shot.entity']
                    ),
                    i_cgt_variants
                )
            )
        return list_

    def shot(self, name, **kwargs):
        t_tw = self._stage._tw

        filters = [['shot.entity', '=', name]]

        cgt_dtb = self._cgt_variants['project.database']
        cgt_type = 'shot'

        id_list = t_tw.info.get_id(cgt_dtb, cgt_type, filters)
        if id_list:
            cgt_variants = t_tw.info.get(
                cgt_dtb, cgt_type,
                id_list, t_tw.info.fields(cgt_dtb, cgt_type)
            )[0]
            return _shot.Shot(
                self._root,
                dict(
                    project=self._variants['project'],
                    episode=cgt_variants.get('eps.entity'),
                    sequence=cgt_variants.get('seq.entity'),
                    shot=cgt_variants['shot.entity']
                ),
                cgt_variants
            )
