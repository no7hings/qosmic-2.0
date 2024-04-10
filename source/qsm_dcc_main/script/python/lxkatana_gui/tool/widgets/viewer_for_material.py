# coding:utf-8
import lxtool.viewer.gui.abstracts as vwr_gui_abstracts

import lxbasic.log as bsc_log

import lxbasic.core as bsc_core
# katana
import lxkatana.core as ktn_core
# katana dcc
import lxkatana.dcc.objects as ktn_dcc_objects

import lxkatana.dcc.operators as ktn_dcc_operators
# katana fnc
import lxkatana.fnc.objects as ktn_fnc_objects


class PnlViewerForMaterialDcc(vwr_gui_abstracts.AbsPnlViewerForMaterialDcc):
    DCC_SCENE_CLS = ktn_dcc_objects.Scene
    DCC_FNC_LOOK_IMPORTER_CLS = ktn_fnc_objects.FncImporterForLookAssOld
    DCC_SELECTION_CLS = ktn_dcc_objects.Selection
    DCC_STAGE_SELECTION_CLS = ktn_core.KtnSGSelectionOpt
    #
    DCC_NAMESPACE = 'dcc'
    #
    DCC_GEOMETRY_TYPES = [
        'subdmesh',
        'renderer procedural'
    ]
    DCC_GEOMETRY_ROOT = '/root/world/geo/master'
    #
    DCC_MATERIAL_TYPES = [
        'material'
    ]
    DCC_MATERIAL_ROOT = '/root/materials'
    #
    DCC_MATERIALS_CLS = ktn_dcc_objects.Materials

    def __init__(self, *args, **kwargs):
        super(PnlViewerForMaterialDcc, self).__init__(*args, **kwargs)

    def post_setup_fnc(self):
        ns = ktn_dcc_operators.LookOutputOpt.get_all_source_nodes()
        p = self._options_prx_node.get_port('dcc.node')
        if ns:
            p.set(
                [i.get_path() for i in ns]
            )

    def _set_dcc_objs_update_from_scene_(self):
        self._scene_obj_scene = self.DCC_SCENE_CLS()

        self._scene_geometry_objs = []

        node_path = self._options_prx_node.get('dcc.node')
        if not node_path:
            return
        obj_opt = ktn_core.NGNodeOpt(node_path)

        self._scene_obj_scene.load_from_location(
            ktn_obj=obj_opt.get_name(),
            root=self._options_prx_node.get('dcc.geometry_root')
        )
        self._scene_obj_scene.load_from_location(
            ktn_obj=obj_opt.get_name(),
            root=self._options_prx_node.get('dcc.material_root')
        )

        self._scene_obj_universe = self._scene_obj_scene.universe
        #
        self._scene_geometry_root = self._scene_obj_universe.get_obj(self.DCC_GEOMETRY_ROOT)
        geometry_types = [self._scene_obj_universe.get_obj_type(i) for i in self.DCC_GEOMETRY_TYPES]
        for geometry_type in geometry_types:
            if geometry_type is not None:
                self._scene_geometry_objs.extend(
                    geometry_type.get_objs()
                )
        #
        self._scene_material_objs = []
        #
        self._scene_material_root = self._scene_obj_universe.get_obj(self.DCC_MATERIAL_ROOT)
        material_types = [self._scene_obj_universe.get_obj_type(i) for i in self.DCC_MATERIAL_TYPES]
        for material_type in material_types:
            if material_type is not None:
                self._scene_material_objs.extend(
                    material_type.get_objs()
                )

    def _set_dcc_obj_guis_build_(self):
        def add_geometry_gui_fnc_(geometry_obj_):
            def select_material_fnc_():
                if _material_obj is not None:
                    self.DCC_SELECTION_CLS([_material_obj.path]).select_all()

            #
            def select_nmc_material_fnc_():
                if _material_obj is not None:
                    _nmc_material_obj = nmc_material_dict[_material_scene_graph_path]
                    self.DCC_SELECTION_CLS([_nmc_material_obj.path]).select_all()

            #
            def select_nme_material_fnc_():
                if _material_obj is not None:
                    _nme_material_obj = nme_material_dict[_material_scene_graph_path]
                    self.DCC_SELECTION_CLS([_nme_material_obj.path]).select_all()

            #
            def get_nme_material_is_exists_fnc():
                return _material_scene_graph_path in nme_material_dict

            #
            def expanded_shaders_fnc_():
                if _material_obj is not None:
                    objs = _material_obj.get_all_source_objs()
                    [ktn_core.NGNodeOpt(i.ktn_obj).set_shader_gui_expanded() for i in objs]

            #
            def collapsed_shaders_fnc_():
                if _material_obj is not None:
                    objs = _material_obj.get_all_source_objs()
                    [ktn_core.NGNodeOpt(i.ktn_obj).set_shader_gui_collapsed() for i in objs]

            #
            def colour_shaders_fnc_():
                if _material_obj is not None:
                    _material_obj.set_source_objs_colour()

            #
            def layout_shaders_with_expanded_fnc_():
                if _material_obj is not None:
                    ktn_core.NGNodeOpt(_material_obj.ktn_obj).gui_layout_shader_graph(size=(320, 960), expanded=True)

            #
            def layout_shaders_with_collapsed_fnc_():
                if _material_obj is not None:
                    ktn_core.NGNodeOpt(_material_obj.ktn_obj).gui_layout_shader_graph(size=(320, 240), collapsed=True)

            #
            geometry_obj_.set_gui_attribute(
                'gui_menu',
                [
                    ('Select material', None, select_material_fnc_),
                    (),
                    ('Select material in "NetworkMaterialCreate"', None, select_nmc_material_fnc_),
                    ('Select material in "NetworkMaterialEdit"', None,
                     (get_nme_material_is_exists_fnc, select_nme_material_fnc_, False)),
                    (),
                    ('Expanded shader(s)', None, expanded_shaders_fnc_),
                    ('Collapsed shader(s)', None, collapsed_shaders_fnc_),
                    (),
                    ('Colour shader(s)', None, colour_shaders_fnc_),
                    (),
                    ('Layout shader(s) with expanded', None, layout_shaders_with_expanded_fnc_),
                    ('Layout shader(s) with collapsed', None, layout_shaders_with_collapsed_fnc_),
                ]
            )
            #
            _geometry_obj_gui = self._prx_dcc_obj_tree_view_add_opt.gui_add_as(
                i_geometry_node, mode='list'
            )
            #
            _obj_opt = geometry_obj_.obj_opt
            _material_scene_graph_path = _obj_opt.get_port_raw('materialAssign')
            if _material_scene_graph_path is not None:
                _sub_material_key = bsc_core.PthNodeOpt(_material_scene_graph_path).name
                _material_obj = material_dict[_material_scene_graph_path]
            else:
                _geometry_obj_gui.check_state.set('ignore')
                _sub_material_key = 'non-exists'
                _material_obj = None
            #
            _material_tag_filter_key = '{}.{}'.format(geometry_obj_.type.name, _sub_material_key)
            #
            self._prx_dcc_obj_tree_view_tag_filter_opt.set_tgt_item_tag_update(
                _material_tag_filter_key,
                _geometry_obj_gui,
                dcc_obj=_material_obj
            )
            _geometry_obj_gui.set_name(_sub_material_key, self.DESCRIPTION_INDEX)
            _material_color = bsc_core.RawTextOpt(_sub_material_key).to_rgb()
            _geometry_obj_gui.set_icon_by_color(_material_color, self.DESCRIPTION_INDEX)

        #
        self._prx_dcc_obj_tree_view_add_opt.restore_all()
        #
        methods = [
            self._set_dcc_objs_update_from_scene_,
        ]
        if methods:
            with bsc_log.LogProcessContext.create(maximum=len(methods), label='execute gui method') as g_p:
                for i_method in methods:
                    g_p.do_update()
                    i_method()
        #
        geometry_objs = self._scene_geometry_objs
        if geometry_objs:
            material_dict = ktn_dcc_objects.Materials.get_material_dict()
            nmc_material_dict = ktn_dcc_objects.Materials.get_nmc_material_dict()
            nme_material_dict = ktn_dcc_objects.Materials.get_nme_material_dict()
            with bsc_log.LogProcessContext.create(maximum=len(geometry_objs), label='gui-add for geometry') as g_p:
                for i_geometry_node in geometry_objs:
                    g_p.do_update()
                    add_geometry_gui_fnc_(i_geometry_node)
