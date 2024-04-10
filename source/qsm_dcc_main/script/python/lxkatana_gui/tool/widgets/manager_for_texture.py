# coding:utf-8
import lxkatana.core as ktn_core

import lxkatana.dcc.objects as ktn_dcc_objects

import lxkatana.dcc.operators as ktn_dcc_operators

import lxtool.manager.gui.abstracts as mng_gui_abstracts


class PnlManagerForTextureSpaceDcc(mng_gui_abstracts.AbsPnlManagerForTextureSpaceDcc):
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection
    DCC_NAMESPACE = 'katana'

    def __init__(self, session, *args, **kwargs):
        super(PnlManagerForTextureSpaceDcc, self).__init__(session, *args, **kwargs)

    def _set_dcc_scene_update_(self):
        self._file_path = ktn_dcc_objects.Scene.get_current_file_path()

    def _set_dcc_texture_references_update_(self):
        self._dcc_texture_references = ktn_dcc_objects.TextureReferences()

    def _set_dcc_objs_update_(self):
        if self._dcc_texture_references is not None:
            root = self._options_prx_node.get('dcc.location')
            geometry_location = '/root/world/geo'
            w_s = ktn_core.WorkspaceSetting()
            opt = w_s.get_current_look_output_opt_force()
            if opt is None:
                return

            s = ktn_dcc_operators.LookOutputOpt(opt)
            location = '{}{}'.format(geometry_location, root)
            dcc_shaders = s.get_all_dcc_geometry_shaders_by_location(location)
            self._dcc_objs = self._dcc_texture_references.get_objs(
                include_paths=[i.path for i in dcc_shaders]
            )


class PnlManagerForAssetTextureDcc(mng_gui_abstracts.AbsPnlManagerForAssetTextureDcc):
    """
    # coding:utf-8
    import lxkatana

    lxkatana.set_reload()
    import lxsession.commands as ssn_commands; ssn_commands.execute_hook("dcc-tool-panels/gen-asset-dcc-texture-manager")
    """
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection
    DCC_NAMESPACE = 'maya'

    def __init__(self, *args, **kwargs):
        super(PnlManagerForAssetTextureDcc, self).__init__(*args, **kwargs)

    def post_setup_fnc(self):
        ns = ktn_dcc_operators.LookOutputOpt.get_look_output_node_opts()
        p = self._options_prx_node.get_port('dcc.node')
        if ns:
            p.set(
                [i.get_path() for i in ns]
            )

    def _set_dcc_texture_references_update_(self):
        self._dcc_texture_references = ktn_dcc_objects.TextureReferences()

    def _set_dcc_objs_update_(self):
        self._dcc_objs = []
        if self._dcc_texture_references is not None:
            node_path = self._options_prx_node.get('dcc.node')
            if node_path:
                obj_opt = ktn_core.NGNodeOpt(node_path)
                scheme = self._options_prx_node.get('scheme')
                scp = ktn_dcc_operators.LookOutputOpt(obj_opt)
                geometry_location_sub = self._options_prx_node.get('dcc.location')
                geometry_location = '/root/world/geo'
                location = '{}{}'.format(geometry_location, geometry_location_sub)
                print scheme
                if scheme == 'assignment':
                    dcc_shaders = scp.get_all_dcc_geometry_shaders_by_location(location)
                elif scheme == 'all':
                    dcc_shaders = scp.get_all_dcc_shaders()
                else:
                    raise RuntimeError()

                self._dcc_objs = self._dcc_texture_references.get_objs(
                    include_paths=[i.path for i in dcc_shaders]
                )
