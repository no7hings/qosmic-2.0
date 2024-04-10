# coding:utf-8
import lxbasic.log as bsc_log
# katana
from .. import core as ktn_core


class ScpWorkspaceCreateNew(object):
    """
# coding:utf-8
import lxkatana

lxkatana.set_reload()

import lxkatana.core as ktn_core

import lxkatana.scripts as ktn_scripts

ktn_scripts.ScpWorkspaceCreateNew.new()
    """
    KEY = 'workspace'

    def __init__(self, obj_opt):
        self._obj_opt = obj_opt

    @classmethod
    def load_geometry_auto(cls):
        g_ns = ktn_core.NGNodesMtd.filter_nodes(
            filters=[('node_type', 'is', 'Group'), ('type', 'in', {'AssetGeometry_Wsp'})]
        )
        if g_ns:
            g_n = g_ns[0]
            g_n_opt = ktn_core.NGNodeOpt(g_n)
            g_n_opt.set(
                'parameters.usd_variant.mode', 'override'
            )
            g_n_opt.execute_port(
                'parameters.usd.tools', index=1
            )

    @classmethod
    def load_look_auto(cls):
        m_gs = ktn_core.NGNodesMtd.filter_nodes(
            filters=[
                ('node_type', 'is', 'GroupMerge'),
                ('user.type', 'in', {'MaterialGroup_Wsp', 'MaterialGroup_Wsp_Usr'})
            ]
        )
        if m_gs:
            m_g = m_gs[0]
            ktn_core.NGNodeOpt(m_g).execute_port('user.parameters.ass.tools', index=0)
            ktn_core.NGNodeOpt(m_g).execute_port('user.parameters.ass.tools', index=1)
        #
        ma_gs = ktn_core.NGNodesMtd.filter_nodes(
            filters=[
                ('node_type', 'is', 'GroupStack'),
                ('user.type', 'in', {'MaterialAssignGroup_Wsp', 'MaterialAssignGroup_Wsp_Usr'})
            ]
        )
        if ma_gs:
            ms_g = ma_gs[0]
            ktn_core.NGNodeOpt(ms_g).execute_port('user.parameters.ass.tools', index=0)
            ktn_core.NGNodeOpt(ms_g).execute_port('user.parameters.ass.tools', index=1)
        #
        gpa_gs = ktn_core.NGNodesMtd.filter_nodes(
            filters=[
                ('node_type', 'is', 'GroupStack'),
                ('user.type', 'in', {'GeometryPropertiesAssignGroup_Wsp', 'GeometryPropertiesAssignGroup_Wsp_Usr'})
            ]
        )
        if gpa_gs:
            gpa_g = gpa_gs[0]
            ktn_core.NGNodeOpt(gpa_g).execute_port('user.parameters.ass.tools', index=0)
            ktn_core.NGNodeOpt(gpa_g).execute_port('user.parameters.ass.tools', index=1)

    @classmethod
    def new(cls):
        def post_fnc_():
            bsc_log.Log.ENABLE = False
            s = ScpWorkspaceCreateNew(obj_opt)
            s.load_geometry_auto()
            s.load_look_auto()
            bsc_log.Log.ENABLE = True

        #
        ktn_obj, i_create = ktn_core.NGNodeOpt._generate_node_create_args(
            '/rootNode/workspace', 'Workspace_Wsp'
        )
        if i_create is True:
            obj_opt = ktn_core.NGNodeOpt(ktn_obj)
            obj_opt.execute_port(
                'workspace.tools', index=0
            )
            #
            # timer = threading.Timer(.25, post_fnc_)
            # timer.start()
            post_fnc_()
