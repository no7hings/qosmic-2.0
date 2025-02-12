# coding:utf-8
from __future__ import print_function

import six

import copy
# noinspection PyUnresolvedReferences
import maya.cmds as cmds
# noinspection PyUnresolvedReferences
import maya.mel as mel

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

from . import time_ as _time

from . import node_for_dag as _node_for_dag


class GeometryCache(object):
    """
    doCreateGeometryCache 6 { "3", "0", "120", "OneFile", "1", "Z:/temeporaries/dongchangbao/cfx/test_1.v001/cache/mcx","0","","0", "add", "0", "1", "1","0","1","mcx","0" } ;
    """

    @classmethod
    def create(
        cls, file_path, location, frame_range, frame_step=1,
        distribution='OneFile'
    ):
        file_opt = bsc_storage.StgFileOpt(file_path)

        start_frame, end_frame = _time.Frame.to_frame_range(frame_range)
        kwargs = dict(
            directory=file_opt.directory_path, fileName=file_opt.name_base,
            startTime=start_frame, endTime=end_frame,
            cacheableNode=location,
            format=distribution, cacheFormat=file_opt.ext[1:], sampleMultiplier=frame_step
        )
        cmds.cacheFile(
            **kwargs
        )

    @classmethod
    def create_and_assign(cls):
        pass


class GeometryCacheOpt(object):
    """
doCreateGeometryCache 6 { "3", "0", "120", "OneFile", "1", "Z:/temeporaries/dongchangbao/cfx/test_2.v002/cache/mcx","0","carol_Skin","0", "add", "0", "1", "1","0","1","mcx","0" } ;
cacheFile -attachFile -fileName "carol_Skin" -directory "Z:/temeporaries/dongchangbao/cfx/test_2.v002/cache/mcx/"  -cacheFormat "mcx"  -cnm "carol_Skin:outputCloth2" -ia cacheSwitch2.inp[0];
    """
    @classmethod
    def _to_locations(cls, arg):
        if arg is not None:
            if isinstance(arg, six.string_types):
                return [_node_for_dag.DagNode.to_path(arg)]
            elif isinstance(arg, (tuple, list)):
                return list([_node_for_dag.DagNode.to_path(x) for x in arg])
            else:
                raise TypeError()
        return []

    def __init__(
        self,
        file_path,
        location=None,
        frame_range=None,
        frame_step=None,

    ):
        self._file_path = file_path
        self._locations = self._to_locations(location)

        self._star_frame, self._end_frame = _time.Frame.to_frame_range(frame_range)
        self._frame_step = frame_step

    def create_and_assign(self):
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
        file_opt = bsc_storage.StgFileOpt(self._file_path)
        kwargs = dict(
            directory=file_opt.directory_path,
            file_name_base=file_opt.name_base,
            start_frame=self._star_frame,
            end_frame=self._end_frame,
            frame_step=self._frame_step,
            cache_format=file_opt.ext[1:],
            distribution='OneFile',
            action='replace',
            force=1
        )

        cmds.select(self._locations)

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

        # print(mel_script)

        return mel.eval(mel_script)


