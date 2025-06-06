# coding:utf-8
from __future__ import print_function
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import lxbasic.storage as bsc_storage

from . import time_ as _time

from . import attribute as _attribute

from . import connection as _connection

from . import shape as _shape

from . import viewport as _viewport


class GeometryCache(object):
    """
doCreateGeometryCache 6 { "3", "0", "120", "OneFile", "1", "Z:/temeporaries/dongchangbao/cfx/test_2.v002/cache/mcx","0","carol_Skin","0", "add", "0", "1", "1","0","1","mcx","0" } ;
cacheFile -attachFile -fileName "carol_Skin" -directory "Z:/temeporaries/dongchangbao/cfx/test_2.v002/cache/mcx/"  -cacheFormat "mcx"  -cnm "carol_Skin:outputCloth2" -ia cacheSwitch2.inp[0];
    """
    @classmethod
    def do_create_and_assign(cls, mcx_path, meshes, nclothes, conditions, frame_range, frame_step):
        """
        //	$args[0] = time range mode:
        //		time range mode = 0 : use $args[1] and $args[2] as start-end
        //		time range mode = 1 : use render globals
        //		time range mode = 2 : use timeline
        //  $args[1] = start frame (if time range mode == 0)
        //  $args[2] = end frame (if time range mode == 0)
        //
        // $version == 2:
        //  $args[3] = cache file distribution, either "OneFile" or "OneFilePerFrame"
        //	$args[4] = 0/1, whether to refresh during caching
        //  $args[5] = directory for cache files, if "", then use project data dir
        //	$args[6] = 0/1, whether to create a cache per geometry
        //	$args[7] = name of cache file. An empty string can be used to specify that an auto-generated name is acceptable.
        //	$args[8] = 0/1, whether the specified cache name is to be used as a prefix
        // $version == 3:
        //  $args[9] = action to perform: "add", "replace", "merge", "mergeDelete" or "export"
        //  $args[10] = force save even if it overwrites existing files
        //	$args[11] = simulation rate, the rate at which the cloth simulation is forced to run
        //	$args[12] = sample mulitplier, the rate at which samples are written, as a multiple of simulation rate.
        //
        //  $version == 4:
        //	$args[13] = 0/1, whether modifications should be inherited from the cache about to be replaced. Valid
        //				only when $action == "replace".
        //	$args[14] = 0/1, whether to store doubles as floats
        //  $version == 5:
        //	$args[15] = name of cache format
        //  $version == 6:
        //	$args[16] = 0/1, whether to export in local or world space
        """
        if not meshes:
            return

        # clear exists
        _viewport.ViewPanels.isolate_select(False)
        cmds.select(meshes)
        _viewport.ViewPanels.isolate_select_for(filter(None, [_shape.Shape.get_transform(x) for x in meshes]), True)

        file_opt = bsc_storage.StgFileOpt(mcx_path)

        star_frame, end_frame = _time.Frame.to_frame_range(frame_range)
        kwargs = dict(
            directory=file_opt.directory_path,
            file_name_base=file_opt.name_base,
            start_frame=star_frame,
            end_frame=end_frame,
            frame_step=frame_step,
            cache_format=file_opt.ext[1:],
            distribution='OneFile',
            action='replace',
            force=1
        )

        mel_script = (
            'doCreateGeometryCache 6 {{'
            ' "3",'                 # 0
            ' "{start_frame}",'     # 1
            ' "{end_frame}",'       # 2
            ' "{distribution}",'    # 3
            ' "1",'                 # 4
            ' "{directory}",'       # 5
            ' "0",'                 # 6
            ' "{file_name_base}",'  # 7
            ' "0",'                 # 8
            ' "{action}",'          # 9
            ' "{force}",'           # 10
            ' "1",'                 # 11
            ' "{frame_step}",'      # 12
            ' "0",'                 # 13
            ' "1",'                 # 14
            ' "{cache_format}",'    # 15
            ' "0" '                 # 16
            '}} ;'
        ).format(**kwargs)

        # disable condition
        if conditions:
            for i in conditions:
                i_connections = _attribute.NodeAttribute.break_targets(
                    i, 'outColor.outColorR', ignore_reference=False
                )
                if i_connections:
                    _attribute.NodeAttribute.create_as_dict(
                        i, 'qsm_connection_records', i_connections
                    )

        # noinspection PyBroadException
        try:
            result = mel.eval(mel_script)
        except Exception:
            result = None

        # turn off dynamic
        if nclothes:
            for i in nclothes:
                _attribute.NodeAttribute.set_value(i, 'isDynamic', 0)

        _viewport.ViewPanels.isolate_select(False)
        return result

    @classmethod
    def do_delete(cls, meshes, nclothes, conditions):
        """
        deleteCacheFile 3 { "keep", "", "geometry" } ;
        @return:
        """
        if not meshes:
            return

        cmds.select(meshes)

        kwargs = dict(

        )

        mel_script = (
            'deleteCacheFile 3 {{'
            ' "keep",'
            ' "",'
            ' "geometry" '
            '}} ;'.format(
                **kwargs
            )
        )

        # noinspection PyBroadException
        try:
            result = mel.eval(mel_script)
        except Exception:
            result = None

        # turn on dynamic
        if nclothes:
            for i in nclothes:
                _attribute.NodeAttribute.set_value(i, 'isDynamic', 1)

        # enable dynamic
        if conditions:
            for i in conditions:
                if _attribute.NodeAttribute.is_exists(i, 'qsm_connection_records'):
                    i_connections = _attribute.NodeAttribute.get_as_dict(i, 'qsm_connection_records')
                    if i_connections:
                        for j in i_connections:
                            _connection.Connection.create(*j)

        return result
