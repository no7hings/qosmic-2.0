# coding:utf-8
import functools
import os
# noinspection PyUnresolvedReferences
import maya.cmds as cmds

import lxbasic.core as bsc_core

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import qsm_general.core as qsm_gnl_core

from ... import core as _mya_core

from ...general import core as _gnl_core

from ...resource import core as _rsc_core

from ...motion import core as _mtn_core

from .. import core as _core


class DynamicGpuCacheOpt(_rsc_core.ResourceScriptOpt):
    CACHE_ROOT = _gnl_core.ResourceCacheNodes.DynamicGpuRoot
    CACHE_NAME = _gnl_core.ResourceCacheNodes.DynamicGpuName

    def __init__(self, *args, **kwargs):
        super(DynamicGpuCacheOpt, self).__init__(*args, **kwargs)

        self._root = self._resource.get_root()

    def export_source(self, file_path):
        if self._root is not None:
            bsc_core.BscStorage.create_directory(
                os.path.dirname(file_path)
            )
            _mya_core.SceneFile.export_file(
                file_path, self._root, keep_reference=True
            )

    def export_motion(self):
        if self._root is not None:
            motion = _mtn_core.AdvCharacterMotionOpt(self._namespace).get_data(control_set_includes=['body', 'face'])
            key = bsc_core.BscHash.to_hash_key(motion)
            directory_path = qsm_gnl_core.MayaCache.generate_dynamic_gpu_directory(key=key)
            motion_file_path = '{}/motion.json'.format(directory_path)
            cache_file_path = '{}/gpu.ma'.format(directory_path)
            if os.path.isfile(motion_file_path) is False:
                _mtn_core.AdvCharacterMotionOpt(self._namespace).export_to(
                    motion_file_path, control_set_includes=['body', 'face']
                )
                return True, motion_file_path, cache_file_path
            return False, motion_file_path, cache_file_path

    def load_cache(self, cache_file_path):
        self.create_cache_root_auto()

        cache_location_new = '{}|{}:{}'.format(self.CACHE_ROOT, self._namespace, self.CACHE_NAME)
        cache_location = '|{}:{}'.format(self._namespace, self.CACHE_NAME)
        if cmds.objExists(cache_location) is False and cmds.objExists(cache_location_new) is False:
            if os.path.isfile(cache_file_path) is True:
                _mya_core.SceneFile.import_file_ignore_error(
                    cache_file_path, namespace=self._namespace
                )
                cmds.setAttr(
                    '{}.qsm_cache'.format(cache_location), cache_location, type='string'
                )
                cmds.parent(cache_location, self.CACHE_ROOT)

                self.remove_resource_auto()

        statistics = bsc_storage.Statistics.generate()
        statistics.update_at_time(
            dict(
                method='dynamic_gpu_cache_load',
                cache=cache_file_path
            )
        )

    def remove_resource_auto(self):
        cache_location = '{}|{}:{}'.format(self.CACHE_ROOT, self._namespace, self.CACHE_NAME)

        layer_name = '{}_dynamic_gpu_hide'.format(self._namespace)
        layer_path = cmds.createDisplayLayer(name=layer_name, number=1, empty=True)
        cmds.editDisplayLayerMembers(layer_path, self._root)
        cmds.setAttr(layer_path+'.visibility', False)

        cmds.container(cache_location, edit=1, force=1, addNode=[layer_path])

        skin_proxy_cache_locations = cmds.ls(
            '{}:{}'.format(self._namespace, _core.RigConfigure.SkinProxyCacheName), long=1
        )
        if skin_proxy_cache_locations:
            cmds.editDisplayLayerMembers(layer_path, *skin_proxy_cache_locations)

    def generate_args(self, start_frame, end_frame, use_motion=False):
        # remove first
        self._resource.remove_skin_proxy()
        task_name = '[dynamic-gpu-cache][{}][{}]'.format(
            self._namespace, '{}-{}'.format(start_frame, end_frame)
        )
        if use_motion is True:
            create_flag, motion_file_path, cache_file_path = self.export_motion()
            if create_flag is True:
                rig_file_path = self._resource.file
                cmd_script = qsm_gnl_core.MayaCacheProcess.generate_command(
                    (
                        'method=dynamic-gpu-cache-generate'
                        '&file={file}&cache_file={cache_file}&namespace={namespace}'
                        '&start_frame={start_frame}&end_frame={end_frame}'
                        '&motion_file={motion_file}&use_motion=True'
                    ).format(
                        file=rig_file_path,
                        cache_file=cache_file_path,
                        namespace=self._namespace,
                        start_frame=start_frame, end_frame=end_frame,
                        motion_file=motion_file_path
                    )
                )
                return task_name, cmd_script, cache_file_path
            return task_name, None, cache_file_path

        directory_path = qsm_gnl_core.MayaCache.generate_dynamic_gpu_local_directory()
        source_file_path = '{}/source.ma'.format(directory_path)
        self.export_source(source_file_path)
        cache_file_path = '{}/gpu.ma'.format(directory_path)
        cmd_script = qsm_gnl_core.MayaCacheProcess.generate_command(
            (
                'method=dynamic-gpu-cache-generate'
                '&file={file}&cache_file={cache_file}&namespace={namespace}'
                '&start_frame={start_frame}&end_frame={end_frame}'
                '&use_motion=False'
            ).format(
                file=source_file_path,
                cache_file=cache_file_path,
                namespace=self._namespace,
                start_frame=start_frame, end_frame=end_frame,
            )
        )
        return task_name, cmd_script, cache_file_path

    @classmethod
    def _load_delay_fnc(cls, task_window, resources, start_frame, end_frame, use_motion):
        with task_window.gui_progressing(maximum=len(resources)) as g_p:
            for i_resource in resources:
                i_resource_opt = cls(i_resource)
                i_task_name, i_cmd_script, i_cache_path = i_resource_opt.generate_args(
                    start_frame, end_frame, use_motion
                )
                if i_cmd_script is not None:
                    task_window.submit(
                        'dynamic_gpu_generate_process',
                        i_task_name,
                        i_cmd_script,
                        completed_fnc=functools.partial(i_resource_opt.load_cache, i_cache_path)
                    )
                else:
                    i_resource_opt.load_cache(i_cache_path)

                g_p.do_update()

    @classmethod
    def load_auto(cls, **kwargs):
        scheme = kwargs['scheme']
        use_motion = kwargs.get('use_motion', False)
        start_frame_, end_frame_ = _mya_core.Frame.get_frame_range()
        start_frame = kwargs.get('start_frame', start_frame_)
        end_frame = kwargs.get('end_frame', end_frame_)
        if scheme == 'default':
            resources = []
            namespaces = _mya_core.Namespaces.extract_roots_from_selection()
            if namespaces:
                resources_query = _core.AdvRigsQuery()
                resources_query.do_update()
                for i_namespace in namespaces:
                    i_resource = resources_query.get(i_namespace)
                    if i_resource:
                        if i_resource.is_dynamic_gpu_exists() is False:
                            resources.append(i_resource)

            if not resources:
                gui_core.GuiDialog.create(
                    '动态GPU加载',
                    content='选择一个或多个可用的角色（如果选中的绑定加载动态GPU了，会被忽略），可以选择绑定的任意部件。',
                    status=gui_core.GuiDialog.ValidationStatus.Warning,
                    no_label='关闭',
                    ok_visible=False, no_visible=True, cancel_visible=False,
                )
                return

            import lxgui.proxy.widgets as gui_prx_widgets

            task_window = gui_prx_widgets.PrxSprcTaskWindow()
            if task_window._language == 'chs':
                task_window.set_window_title('动态GPU加载')
                task_window.set_tip(
                    '动态GPU会在后台生成，生成成功后会自动加载到场景中，请耐心等待；\n'
                    '生成后台任务之前会把选中的绑定+动画导出，这个过程会占用比较长的时间；\n'
                    '这个过程可能会让MAYA前台操作产生些许卡顿；\n'
                    '如需要终止任务，请点击“关闭”。'
                )
            else:
                task_window.set_window_title('Dynamic GPU Load')

            task_window.show_window_auto(exclusive=False)
            task_window.run_fnc_delay(
                functools.partial(
                    cls._load_delay_fnc,
                    task_window, resources, start_frame, end_frame, use_motion),
                500
            )


class DynamicGpuCacheGenerate(object):
    CACHE_ROOT = '|__DYNAMIC_GPU__'

    CACHE_NAME = _core.RigConfigure.DynamicGpuCacheName

    @classmethod
    def _export_gpu_frame(cls, location, gpu_file_path, start_frame, end_frame, with_material=False):
        cmds.loadPlugin('gpuCache', quiet=1)
        if cmds.objExists(location):
            directory_path = os.path.dirname(gpu_file_path)
            file_name = os.path.splitext(os.path.basename(gpu_file_path))[0]
            cmds.gpuCache(
                location,
                startTime=start_frame, endTime=end_frame,
                optimize=1, optimizationThreshold=40000,
                writeMaterials=with_material,
                dataFormat='ogawa',
                directory=directory_path,
                fileName=file_name
            )

    @classmethod
    def _export_gpu(cls, location, gpu_file_path, start_frame, end_frame, with_material=False):
        frame_range = range(start_frame, end_frame+1)
        seq_range = range(end_frame-start_frame+1)
        with bsc_log.LogProcessContext.create(maximum=len(seq_range)) as l_p:
            for i_seq in seq_range:
                i_frame = frame_range[i_seq]
                i_frame_seq = i_seq+1
                i_gpu_file_path = ('.'+str(i_frame_seq).zfill(4)).join(os.path.splitext(gpu_file_path))
                cls._export_gpu_frame(location, i_gpu_file_path, i_frame, i_frame, with_material)
                l_p.do_update()

    @classmethod
    def _get_unit_conversions(cls, path):
        return list(
            set(
                cmds.listConnections(
                    path, destination=0, source=1, type='timeToUnitConversion'
                ) or []
            )
        )

    @classmethod
    def _build_cache(cls, location, gpu_file_path, start_frame, end_frame):
        if cmds.objExists(location) is True:
            return

        cmds.loadPlugin('gpuCache', quiet=1)
        nodes = []
        frame_count = end_frame - start_frame+1
        # create container
        parent_path = '|'.join(location.split('|')[:-1])
        name = location.split('|')[-1]
        cmds.container(type='dagContainer', name=name)
        if parent_path:
            cmds.parent(name, parent_path)

        cmds.setAttr(location + '.iconName', 'fileNew.png', type='string')

        cmds.addAttr(location, longName='qsm_start_frame', attributeType='long', keyable=1)
        cmds.setAttr(location+'.qsm_start_frame', 1, lock=1)
        cmds.addAttr(location, longName='qsm_end_frame', attributeType='long', keyable=1)
        cmds.setAttr(location+'.qsm_end_frame', frame_count, lock=1)
        cmds.addAttr(location, longName='qsm_index', attributeType='long', keyable=1)
        cmds.addAttr(location, longName='qsm_frame', attributeType='long', keyable=1)
        cmds.connectAttr('time1.outTime', location+'.qsm_frame')
        _mya_core.NodeAttribute.create_as_float(location, 'qsm_speed', 1.0)
        _mya_core.NodeAttribute.create_as_integer(location, 'qsm_offset', -start_frame)

        cmds.addAttr(location, longName='qsm_cache', dataType='string')
        # expression
        eps_name = '{}_eps'.format(name)

        eps_script = (
            '$end_frame={0}.qsm_end_frame;\n'
            '$frame={0}.qsm_frame;\n'
            '$offset={0}.qsm_offset;\n'
            '$speed={0}.qsm_speed;\n'
            '{0}.qsm_index=abs(($frame+$end_frame+$offset)%$end_frame)%$end_frame*$speed+1;'
        ).format(
            location
        )

        eps_path = cmds.expression(
            name=eps_name, string=eps_script, object=location, alwaysEvaluate=1, unitConversion=1
        )
        cmds.setAttr(location+'.qsm_index', lock=1)
        # time conversion
        time_conversion_path = cls._get_unit_conversions(location)[0]
        time_conversion_name_new = '{}_tmc'.format(name)
        cmds.rename(time_conversion_path, time_conversion_name_new)
        nodes.extend([eps_path, time_conversion_name_new])
        # gpu
        for i_seq in range(frame_count):
            i_frame_seq = i_seq+1
            i_seq_str = str(i_seq).zfill(4)
            i_time_range = range(i_frame_seq, i_frame_seq+2)

            i_gpu_file_path = ('.'+str(i_frame_seq).zfill(4)).join(os.path.splitext(gpu_file_path))

            i_gpu_name = '{}_{}_gpu'.format(name, i_seq_str)
            i_gpu_path = '{}|{}'.format(location, i_gpu_name)
            cmds.createNode('gpuCache', name=i_gpu_name, parent=location, skipSelect=1)
            cmds.setAttr(i_gpu_path+'.cacheFileName', i_gpu_file_path, type='string')
            cmds.setAttr(i_gpu_path+'.visibility', keyable=1)

            cmds.addAttr(i_gpu_path, longName='qsm_index', attributeType='long', keyable=1)
            cmds.setAttr(i_gpu_path+'.qsm_index', i_frame_seq)
            nodes.append(i_gpu_path)

            i_cdt_name = '{}_{}_cdt'.format(name, i_seq_str)
            i_cdt_path = i_cdt_name
            cmds.createNode('condition', name=i_cdt_name, skipSelect=1)
            nodes.append(i_cdt_path)
            cmds.connectAttr('{}.qsm_index'.format(location), '{}.firstTerm'.format(i_cdt_path))
            cmds.connectAttr('{}.qsm_index'.format(i_gpu_path), '{}.secondTerm'.format(i_cdt_path))
            cmds.connectAttr('{}.outColor.outColorR'.format(i_cdt_path), i_gpu_path + '.visibility')
            cmds.setAttr('{}.colorIfTrueR'.format(i_cdt_path), 1.0)
            cmds.setAttr('{}.colorIfFalseR'.format(i_cdt_path), 0.0)
        # add nodes
        cmds.setAttr(location+'.blackBox', 1, lock=1)
        cmds.container(location, edit=1, force=1, addNode=nodes)
        # cmds.setAttr(location+'.hiddenInOutliner', 1)

    @classmethod
    def _import_file(cls, file_path, namespace=':'):
        return cmds.file(
            file_path,
            i=True,
            options='v=0;',
            type='mayaAscii',
            ra=True,
            mergeNamespacesOnClash=True,
            namespace=namespace,
        )

    @classmethod
    def _get_display_layers(cls, path):
        return list(
            set(
                cmds.listConnections(
                    path, destination=0, source=1, type='displayLayer'
                ) or []
            )
        )

    @classmethod
    def _clear_display_layers(cls, path):
        _ = cls._get_display_layers(path)
        for i in _:
            cmds.delete(i)

    def __init__(self, namespace):
        self._namespace = namespace
        self._reference_namespace_query = _mya_core.ReferenceNamespacesCache()
        self._resource = _core.AdvRig(self._namespace)
        self._root = self._resource.get_root()
        self._geometry_location = self._resource.get_geometry_root()

    def get_geometry_root(self):
        return self._geometry_location

    def create_cache_root_auto(self):
        if cmds.objExists(self.CACHE_ROOT) is False:
            cmds.createNode(
                'dagContainer', name=self.CACHE_ROOT.split('|')[-1], shared=1, skipSelect=1
            )
            cmds.setAttr(self.CACHE_ROOT+'.iconName', 'folder-closed.png', type='string')

    def export_source(self, file_path):
        if self._root is not None:
            bsc_core.BscStorage.create_directory(
                os.path.dirname(file_path)
            )
            _mya_core.SceneFile.export_file(
                file_path, self._root
            )

    def export_gpu(self, cache_file_path, start_frame, end_frame):
        self._export_gpu(
            self._geometry_location, cache_file_path, start_frame, end_frame
        )

    def create_cache(self, cache_file_path, gpu_file_path, start_frame, end_frame):
        cache_location = '|{}'.format(self.CACHE_NAME)
        self._build_cache(
            cache_location, gpu_file_path, start_frame, end_frame
        )
        _mya_core.SceneFile.export_file(
            cache_file_path, cache_location
        )

    def test(self):
        pass


class DynamicGpuCacheProcess(object):
    KEY = 'dynamic gpu'

    def __init__(self, file_path, cache_file_path, namespace, start_frame, end_frame, motion_file, use_motion):
        self._file_path = file_path
        file_base = os.path.splitext(cache_file_path)[0]
        self._gpu_file_path = '{}.abc'.format(file_base)
        self._cache_file_path = cache_file_path

        self._namespace = namespace

        self._start_frame = start_frame
        self._end_frame = end_frame

        self._motion_file = motion_file
        self._use_motion = use_motion

    def execute(self):
        with bsc_log.LogProcessContext.create(maximum=4) as l_p:
            # step 1
            _mya_core.SceneFile.new()
            l_p.do_update()
            # step 2
            if os.path.isfile(self._file_path) is False:
                raise RuntimeError()

            bsc_log.Log.trace_method_result(
                self.KEY, 'load scene: {}'.format(self._file_path)
            )
            if self._use_motion is False:
                _mya_core.SceneFile.open(self._file_path)
            else:
                _mya_core.SceneFile.reference_file(self._file_path, namespace=self._namespace)
                _mtn_core.AdvCharacterMotionOpt(self._namespace).load_from(
                    self._motion_file, force=True
                )
            l_p.do_update()
            # step 3
            generate = DynamicGpuCacheGenerate(self._namespace)
            geometry_location = generate.get_geometry_root()
            generate._clear_display_layers(geometry_location)
            generate.export_gpu(
                self._gpu_file_path, self._start_frame, self._end_frame
            )
            l_p.do_update()
            # step 4
            generate.create_cache(
                self._cache_file_path, self._gpu_file_path, self._start_frame, self._end_frame
            )
            l_p.do_update()


if __name__ == '__main__':
    pass
