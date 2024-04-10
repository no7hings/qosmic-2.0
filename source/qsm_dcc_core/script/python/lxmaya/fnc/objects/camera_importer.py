# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.fnc.abstracts as bsc_fnc_abstracts
# maya
from ...core.wrap import *

from ... import core as mya_core
# maya dcc
from ...dcc import objects as mya_dcc_objects


class FncImporterForCameraAbc(
    bsc_fnc_abstracts.AbsFncOptionBase
):
    OPTION = dict(
        file='',
        location='',
        namespace=':',
        camera_resolution=(2048, 2048)
    )
    PLUG_NAME = 'AbcImport'
    OBJ_PATHSEP = mya_core.MyaUtil.OBJ_PATHSEP

    def __init__(self, option=None):
        super(FncImporterForCameraAbc, self).__init__(option)

    def set_run(self):
        cmds.loadPlugin(self.PLUG_NAME, quiet=1)
        #
        file_path = self.get('file')
        location = self.get('location')
        #
        namespace_temporary = 'alembic_import_{}'.format(bsc_core.SysBaseMtd.get_time_tag())
        mya_location = bsc_core.PthNodeOpt(location).translate_to(
            self.OBJ_PATHSEP
        ).get_value()
        group = mya_dcc_objects.Group(mya_location)
        group.set_dag_components_create()
        #
        cmds.file(
            file_path,
            i=1,
            options='v=0;',
            type='Alembic',
            ra=1,
            mergeNamespacesOnClash=1,
            namespace=namespace_temporary,
            preserveReferences=1
        )
        #
        namespace_obj = mya_dcc_objects.Namespace(namespace_temporary)
        self._results = []
        objs = namespace_obj.get_objs()
        for i_obj in objs:
            bsc_log.Log.trace_method_result(
                'alembic import',
                u'obj="{}"'.format(i_obj.path)
            )
            if i_obj.type_name == 'transform':
                path_src = i_obj.path
                if len(path_src.split('|')) == 2:
                    i_children = i_obj.get_children()
                    for j_child in i_children:
                        if j_child.type_name == 'camera':
                            j_camera = mya_dcc_objects.Camera(j_child.path)
                            j_camera.set_display_()
                    #
                    target_obj_path = '{}|{}'.format(
                        mya_location, bsc_core.PthNodeMtd.get_dag_name_with_namespace_clear(i_obj.name)
                    )
                    obj_tgt = mya_dcc_objects.Node(target_obj_path)
                    if obj_tgt.get_is_exists() is True:
                        obj_tgt.do_delete()
                    #
                    i_obj.parent_to_path(mya_location)
            #
            i_obj._update_path_()
            dcc_dag_path = bsc_core.PthNodeOpt(i_obj.path).clear_namespace_to()
            self._results.append(dcc_dag_path.path)
        #
        namespace_obj.do_delete()
        return self._results
