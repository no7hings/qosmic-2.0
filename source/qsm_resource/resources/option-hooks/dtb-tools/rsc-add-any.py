# coding:utf-8
import copy

import lxbasic.resource as bsc_resource

import lxbasic.core as bsc_core

import lxbasic.storage as bsc_storage

import lxgui.core as gui_core

import lxgui.proxy.widgets as prx_widgets

import lxbasic.database as bsc_database

import lxuniverse.objects as unv_objects


class ScpRscAddAnyOpt(object):
    def __init__(self, window, options, unr_resource):
        self._window = window
        self._options = options
        self._unr_resource = unr_resource
        self._category_group = unr_resource.properties.get('database.category_group')
        self._category = unr_resource.properties.get('database.category')
        self._type = unr_resource.properties.get('database.type')
        self._type_path = unr_resource.properties.get('database.type_path')

        self._dtb_opt = self._window.get_dtb_opt(self._category_group)

    @classmethod
    def dtb_create_type(cls, dtb_opt, type_dtb_path):
        return dtb_opt.get_type_force(type_dtb_path)

    @classmethod
    def dtb_assign_resource_types_fnc(cls, dtb_opt, resource_dtb_path, type_dtb_paths):
        for i_type_dtb_path in type_dtb_paths:
            dtb_opt.create_type_assign(
                resource_dtb_path, i_type_dtb_path, kind=dtb_opt.Kinds.ResourceType
            )

    @classmethod
    def stg_create_resource(cls, dtb_opt, pattern_kwargs):
        p_opt = dtb_opt.get_pattern_opt('resource-dir')
        stg_path = p_opt.update_variants_to(**pattern_kwargs).get_value()
        path_opt = bsc_storage.StgDirectoryOpt(stg_path)
        path_opt.set_create()
        return stg_path

    @classmethod
    def stg_create_version(cls, dtb_opt, pattern_kwargs):
        p_opt = dtb_opt.get_pattern_opt('version-dir')
        stg_path = p_opt.update_variants_to(**pattern_kwargs).get_value()
        path_opt = bsc_storage.StgDirectoryOpt(stg_path)
        path_opt.set_create()
        return stg_path

    @classmethod
    def dtb_create_version_storage_fnc(cls, dtb_opt, version_dtb_path, version_stg_path, pattern_kwargs):
        dtb_cfg_opt = dtb_opt.get_database_configure_opt()
        data = dtb_cfg_opt.get('storages')
        for i_k, i_v in data.items():
            i_kind = i_v['kind']
            i_keyword = i_v['keyword']
            i_pattern_opt = dtb_opt.get_pattern_opt(i_keyword)
            i_storage_stg_path = i_pattern_opt.update_variants_to(**pattern_kwargs).get_value()
            if i_storage_stg_path.startswith(version_stg_path):
                i_storage_dtb_path = '{}/{}'.format(version_dtb_path, i_k)
                i_is_create, i_dtb_storage = dtb_opt.create_storage(
                    i_storage_dtb_path, i_kind
                )
                if i_is_create is True:
                    # version property
                    dtb_opt.create_property(
                        version_dtb_path, i_k, i_storage_dtb_path, kind=dtb_opt.Kinds.Version
                    )
                    # storage property
                    dtb_opt.create_property(
                        i_storage_dtb_path, 'keyword', i_keyword, kind=i_kind
                    )
                    dtb_opt.create_property(
                        i_storage_dtb_path, 'location', i_storage_stg_path, kind=i_kind
                    )
                    dtb_opt.create_property(
                        i_storage_dtb_path, 'version', version_dtb_path, kind=i_kind
                    )
            else:
                raise RuntimeError()

    @classmethod
    def stg_create_preview(cls, dtb_opt, file_path, pattern_kwargs):
        preview_file_path_ = bsc_storage.ImgOiioOptForThumbnail(file_path).generate_thumbnail(width=256, ext='.png')
        preview_file_p_opt = dtb_opt.get_pattern_opt('image-preview-png-file')
        preview_file_path = preview_file_p_opt.update_variants_to(**pattern_kwargs).get_value()
        bsc_storage.StgFileOpt(preview_file_path_).copy_to_file(
            preview_file_path
        )
        return preview_file_path

    @classmethod
    def create_resource_fnc(cls, dtb_opt, unr_resource, type_path):
        force = True
        resource_dtb_path = unr_resource.get_path()
        pattern_kwargs = unr_resource.properties.get('pattern_kwargs')
        is_create, dtb_resource = dtb_opt.create_resource(resource_dtb_path)
        if is_create is True or force is True:
            resource_stg_path = cls.stg_create_resource(dtb_opt, pattern_kwargs)
            # add properties
            dtb_opt.create_property(
                resource_dtb_path, 'location', resource_stg_path, kind=dtb_opt.Kinds.Resource
            )
            cls.dtb_assign_resource_types_fnc(dtb_opt, resource_dtb_path, [type_path])
        return resource_dtb_path

    @classmethod
    def create_version_fnc(cls, dtb_opt, resource_dtb_path, unr_version):
        version_dtb_path = unr_version.get_path()
        pattern_kwargs = unr_version.properties.get('pattern_kwargs')
        force = True
        is_create, dtb_version = dtb_opt.create_version(version_dtb_path)
        if is_create is True or force is True:
            version_stg_path = cls.stg_create_version(dtb_opt, pattern_kwargs)
            # set version
            dtb_opt.create_property(
                resource_dtb_path, 'version', version_dtb_path, kind=dtb_opt.Kinds.Resource
            )
            # add properties
            dtb_opt.create_property(
                version_dtb_path, 'resource', resource_dtb_path, kind=dtb_opt.Kinds.Version
            )
            dtb_opt.create_property(
                version_dtb_path, 'location', version_stg_path, kind=dtb_opt.Kinds.Version
            )
            cls.dtb_create_version_storage_fnc(dtb_opt, version_dtb_path, version_stg_path, pattern_kwargs)
        return version_dtb_path

    @classmethod
    def create_preview_fnc(cls, dtb_opt, version_dtb_path, unr_preview):
        force = True
        file_path_src = unr_preview.properties.get('storage.file_src')
        pattern_kwargs = unr_preview.properties.get('pattern_kwargs')
        preview_stg_path = cls.stg_create_preview(dtb_opt, file_path_src, pattern_kwargs)
        # version properties
        dtb_opt.create_property(
            version_dtb_path, 'image_preview_file', preview_stg_path, kind=dtb_opt.Kinds.Version
        )
        preview_dtb_path = unr_preview.get_path()
        is_create, dtb_preview = dtb_opt.create_storage(
            preview_dtb_path, kind=dtb_opt.Kinds.File
        )
        if is_create is True or force is True:
            dtb_opt.create_property(
                version_dtb_path, 'preview', preview_dtb_path, kind=dtb_opt.Kinds.Version
            )

    @classmethod
    def create_textures_fnc(cls, dtb_opt, version_dtb_path, unr_textures):
        for i_unr_texture in unr_textures:
            cls.create_texture_fnc(dtb_opt, version_dtb_path, i_unr_texture)

    @classmethod
    def create_texture_fnc(cls, dtb_opt, version_dtb_path, unr_texture):
        keyword = 'texture-original-src-file'
        file_path_src = unr_texture.properties.get('storage.file_src')
        pattern_kwargs = unr_texture.properties.get('pattern_kwargs')
        file_stg_path = cls.stg_create_texture(dtb_opt, file_path_src, pattern_kwargs, keyword)
        key = 'texture_{texture_type_tag}_file'.format(**pattern_kwargs)
        file_dtb_path = '{}/{}'.format(version_dtb_path, key)
        dtb_opt.create_storage(
            file_dtb_path, kind=dtb_opt.Kinds.File
        )
        dtb_opt.create_property(
            version_dtb_path, key, file_dtb_path, kind=dtb_opt.Kinds.Version
        )
        # storage property
        dtb_opt.create_property(
            file_dtb_path, 'keyword', keyword, kind=dtb_opt.Kinds.File
        )
        dtb_opt.create_property(
            file_dtb_path, 'location', file_stg_path, kind=dtb_opt.Kinds.File
        )
        dtb_opt.create_property(
            file_dtb_path, 'version', version_dtb_path, kind=dtb_opt.Kinds.File
        )

    @classmethod
    def stg_create_texture(cls, dtb_opt, file_path_src, pattern_kwargs, keyword):
        p_opt = dtb_opt.get_pattern_opt(keyword)
        stg_path = p_opt.update_variants_to(**pattern_kwargs).get_value()
        bsc_storage.StgFileOpt(file_path_src).copy_to_file(
            stg_path
        )
        return stg_path

    @classmethod
    def create_hdri_fnc(cls, dtb_opt, version_dtb_path, unr_hdri):
        keyword = 'hdri-original-src-file'
        file_path_src = unr_hdri.properties.get('storage.file_src')
        pattern_kwargs = unr_hdri.properties.get('pattern_kwargs')
        file_stg_path = cls.stg_create_hdri(dtb_opt, file_path_src, pattern_kwargs, keyword)
        key = 'hdri_file'
        file_dtb_path = '{}/{}'.format(version_dtb_path, key)
        dtb_opt.create_storage(
            file_dtb_path, kind=dtb_opt.Kinds.File
        )
        dtb_opt.create_property(
            version_dtb_path, key, file_dtb_path, kind=dtb_opt.Kinds.Version
        )
        # storage property
        dtb_opt.create_property(
            file_dtb_path, 'keyword', keyword, kind=dtb_opt.Kinds.File
        )
        dtb_opt.create_property(
            file_dtb_path, 'location', file_stg_path, kind=dtb_opt.Kinds.File
        )
        dtb_opt.create_property(
            file_dtb_path, 'version', version_dtb_path, kind=dtb_opt.Kinds.File
        )

    @classmethod
    def stg_create_hdri(cls, dtb_opt, file_path_src, pattern_kwargs, keyword):
        p_opt = dtb_opt.get_pattern_opt(keyword)
        stg_path = p_opt.update_variants_to(**pattern_kwargs).get_value()
        bsc_storage.StgFileOpt(file_path_src).copy_to_file(
            stg_path
        )
        return stg_path

    def execute(self):
        self.dtb_create_type(self._dtb_opt, self._type_path)
        unr_versions = self._unr_resource.get_children()
        resource_dtb_path = self.create_resource_fnc(
            self._dtb_opt, self._unr_resource, self._type_path
        )
        if unr_versions:
            unr_version = unr_versions[0]
            version_dtb_path = self.create_version_fnc(
                self._dtb_opt, resource_dtb_path, unr_version
            )
            children = unr_version.get_children()

            unr_previews = [i for i in children if i.get_type_name() == 'image']
            if unr_previews:
                unr_preview = unr_previews[0]
                self.create_preview_fnc(
                    self._dtb_opt, version_dtb_path, unr_preview
                )

            unr_textures = [i for i in children if i.get_type_name() == 'texture']
            if unr_textures:
                self.create_textures_fnc(
                    self._dtb_opt, version_dtb_path, unr_textures
                )

            unr_hdris = [i for i in children if i.get_type_name() == 'hdri']
            if unr_hdris:
                unr_hdri = unr_hdris[0]
                self.create_hdri_fnc(
                    self._dtb_opt, version_dtb_path, unr_hdri
                )


class PnlRscTextureAddTool(prx_widgets.PrxSessionWindow):
    IMAGE_KEYS = [
        'preview'
    ]
    TEXTURE_KEYS = [
        'albedo',
        'diffuse',
        'ao',
        'specular',
        'roughness', 'glossiness',
        'coat',
        'coat_roughness',
        'opacity',
        'normal',
        'displacement',
        #
        'mask'
    ]
    HDRI_KEYS = [

    ]

    def apply_fnc(self):
        checked_items = self._node_prx_tree_view._qt_view._get_all_checked_items_()
        unr_resources = [i_item._get_node_() for i_item in checked_items if
                         i_item._get_node_().get_type_name() == 'resource']
        if not unr_resources:
            gui_core.GuiDialog.create(
                self._session.gui_name,
                content='check one or more node and retry',
                status=gui_core.GuiDialog.ValidationStatus.Warning,
                #
                yes_label='Close',
                #
                no_visible=False, cancel_visible=False
            )
        with self.gui_progressing(maximum=len(unr_resources), label='resource create process') as g_p:
            for i_unr_resource in unr_resources:
                g_p.do_update()
                ScpRscAddAnyOpt(self, self._options, i_unr_resource).execute()

    def gui_setup_window(self):
        s_0 = prx_widgets.PrxVScrollArea()
        self.add_widget(s_0)
        h_s = prx_widgets.PrxHSplitter()
        s_0.add_widget(h_s)
        #
        s_1 = prx_widgets.PrxVScrollArea()
        h_s.add_widget(s_1)
        #
        self._options_prx_node = prx_widgets.PrxOptionsNode('options')
        s_1.add_widget(self._options_prx_node)
        self._options_prx_node.create_ports_by_data(
            self._session.configure.get('build.node.options'),
        )
        #
        self._tip_text_browser = prx_widgets.PrxTextBrowser()
        s_1.add_widget(self._tip_text_browser)
        self._tip_text_browser.set_font_size(12)
        self._tip_text_browser.set_content(
            self._session.configure.get('build.node.content'),
        )
        #
        self._options_prx_node.get_port('classification.category_group').connect_input_changed_to(
            self.gui_refresh_dtb_opt
        )
        self._options_prx_node.get_port('classification.category_group').connect_input_changed_to(
            self.gui_refresh_categories
        )
        self._options_prx_node.get_port('classification.category').connect_input_changed_to(
            self.gui_refresh_types
        )
        self._options_prx_node.get_port('classification.category_and_type_use_name').connect_input_changed_to(
            self.gui_refresh
        )
        #
        self._options_prx_node.set('scheme.name', self._session.configure.get_key_names_at('build.schemes'))
        self._options_prx_node.set('scheme.load', self.load_scheme_cbk)
        #
        self._node_prx_tree_view = prx_widgets.PrxNGTree()
        h_s.add_widget(self._node_prx_tree_view)
        h_s.set_fixed_size_at(0, 480)

        self._match_button = prx_widgets.PrxPressButton()
        self._match_button.set_name('match')
        self.add_button(self._match_button)
        self._match_button.connect_press_clicked_to(self.gui_refresh)

        self._add_button = prx_widgets.PrxPressButton()
        self._add_button.set_name('add')
        self.add_button(self._add_button)
        self._add_button.connect_press_clicked_to(self.apply_fnc)

        self.refresh_all()

    def __init__(self, session, *args, **kwargs):
        super(PnlRscTextureAddTool, self).__init__(session, *args, **kwargs)

    def refresh_all(self):
        self.gui_refresh_dtb_opt()
        self.gui_refresh_categories()
        # self.gui_refresh()

    @classmethod
    def get_dtb_opt(cls, category_group):
        return bsc_database.DtbOptForResource(
            bsc_resource.RscExtendConfigure.get_yaml('database/library/resource-basic'),
            bsc_resource.RscExtendConfigure.get_yaml('database/library/resource-{}'.format(category_group))
        )

    def gui_refresh_dtb_opt(self):
        self._dtb_opt = self.get_dtb_opt(self._options_prx_node.get('classification.category_group'))

    def gui_refresh_categories(self):
        category_group = self._options_prx_node.get('classification.category_group')
        dtb_categories = self._dtb_opt.get_categories(
            category_group
        )
        self._options_prx_node.set(
            'classification.category', [i.name for i in dtb_categories]
        )
        self.gui_refresh_types()

    def gui_refresh_types(self):
        category_group = self._options_prx_node.get('classification.category_group')
        category = self._options_prx_node.get('classification.category')
        dtb_types = self._dtb_opt.get_types(
            category_group, category
        )
        self._options_prx_node.set(
            'classification.type', [i.name for i in dtb_types]
        )

    def gui_refresh(self):
        self._universe = unv_objects.ObjUniverse()
        self._unr_resource_type = self._universe.generate_obj_type('database', 'resource')
        self._unr_version_type = self._universe.generate_obj_type('database', 'version')
        self._unr_image_type = self._universe.generate_obj_type('database', 'image')
        self._unr_texture_type = self._universe.generate_obj_type('database', 'texture')
        self._unr_hdri_type = self._universe.generate_obj_type('database', 'hdri')
        self._options = self._options_prx_node.to_dict()
        directory_path = self._options.get('directory')
        if directory_path:
            self._variants = dict(
                directory=directory_path
            )
            self._category_group = self._options.get('classification.category_group')
            self._category = self._options.get('classification.category')
            self._type = self._options.get('classification.type')
            self._type_path = '/'+'/'.join([self._category_group, self._category, self._type])
            #
            self.__unr_add_resources()
            self._node_prx_tree_view.set_universe(
                self._universe
            )
            self._node_prx_tree_view.expand_items_by_depth(
                4
            )

    @classmethod
    def get_matches_by_patterns(cls, pattern_string, variants):
        patterns = map(lambda x: str(x).strip(), pattern_string.split(','))
        for i_pattern in patterns:
            i_pattern_opt = bsc_core.PtnStgParseOpt(i_pattern)
            i_pattern_opt.update_variants(**variants)
            i_matches = i_pattern_opt.get_matches(sort=True)
            if i_matches:
                return i_matches
        return []

    def load_scheme_cbk(self):
        scheme_name = self._options_prx_node.get('scheme.name')
        includes = []
        c = self._session.get_configure()
        # resource
        self._options_prx_node.set(
            'resource.includes', c.get('build.schemes.{}.resource.includes'.format(scheme_name))
        )
        self._options_prx_node.set(
            'resource.name_pattern', c.get('build.schemes.{}.resource.name_pattern'.format(scheme_name))
        )
        self._options_prx_node.set(
            'resource.match_patterns', c.get('build.schemes.{}.resource.match_patterns'.format(scheme_name))
        )
        # classification
        classification_data = c.get('build.schemes.{}.classification'.format(scheme_name))
        if classification_data:
            if 'category_group' in classification_data:
                self._options_prx_node.set(
                    'classification.category_group', classification_data['category_group']
                )
        # image
        image_data = c.get('build.schemes.{}.image'.format(scheme_name))
        if image_data:
            includes.append('image')
            self._options_prx_node.get_port('image').set_expanded(True)
            for i_key in self.IMAGE_KEYS:
                if i_key in image_data:
                    self._options_prx_node.set(
                        'image.{}_enable'.format(i_key), True
                    )
                    self._options_prx_node.set(
                        'image.{}.match_patterns'.format(i_key), image_data[i_key]
                    )
                else:
                    self._options_prx_node.set(
                        'image.{}_enable'.format(i_key), False
                    )
        # texture
        texture_data = c.get('build.schemes.{}.texture'.format(scheme_name))
        if texture_data:
            includes.append('texture')
            self._options_prx_node.get_port('texture').set_expanded(True)
            for i_key in self.TEXTURE_KEYS:
                if i_key in texture_data:
                    self._options_prx_node.set(
                        'texture.{}_enable'.format(i_key), True
                    )
                    self._options_prx_node.set(
                        'texture.{}.match_patterns'.format(i_key), texture_data[i_key]
                    )
                else:
                    self._options_prx_node.set(
                        'texture.{}_enable'.format(i_key), False
                    )
        # hdri
        hdri_data = c.get('build.schemes.{}.hdri'.format(scheme_name))
        if hdri_data:
            includes.append('hdri')
            self._options_prx_node.get_port('hdri').set_expanded(True)

        self._options_prx_node.set('includes', includes)
        self.gui_refresh()

    def __unr_add_resources(self):
        pattern = self._options.get('resource.match_patterns')
        matches = self.get_matches_by_patterns(pattern, self._variants)
        if matches:
            name_pattern = self._options.get('resource.name_pattern')
            include_file_types = self._options.get('resource.includes')
            with self.gui_progressing(maximum=len(matches), label='resource build process') as g_p:
                for i_file_variants in matches:
                    g_p.do_update()
                    i_file_path = i_file_variants['result']
                    i_file_type = ['file', 'directory'][bsc_storage.StgPathMtd.get_is_directory(i_file_path)]
                    if i_file_type not in include_file_types:
                        continue
                    i_resource_n_p_o = bsc_core.PtnStgParseOpt(name_pattern)
                    i_resource_n_p_o.update_variants(**i_file_variants)
                    if not i_resource_n_p_o.get_keys():
                        if self._options.get('resource.reduce_name') is True:
                            i_resource_name = bsc_core.RawTextMtd.clear_up_to(
                                '_'.join(bsc_core.RawTextMtd.split_any_to(i_resource_n_p_o.get_value()))
                            ).strip().lower()
                        else:
                            i_resource_name = i_resource_n_p_o.get_value().strip().lower()

                        self.__unr_add_resource(i_resource_name, i_file_variants)

    def __unr_add_resource(self, resource_name, file_variants):
        resource_dtb_path = '/{}/{}'.format(self._category_group, resource_name)
        version_name = 'v0001'
        pattern_kwargs = dict(
            category_group=self._category_group,
            resource=resource_name,
            version=version_name,
        )
        #
        unr_resource = self._unr_resource_type.create_obj(resource_dtb_path)
        unr_resource.properties.set('pattern_kwargs', pattern_kwargs)
        unr_resource.properties.set('database.category_group', self._category_group)
        if self._options.get('classification.category_and_type_use_name') is True:
            keys = bsc_core.RawTextMtd.find_words(resource_name)
            type_args = self._dtb_opt.guess_type_args(
                [self._category_group]+keys
            )
            category_over, type_over = type_args[1:]
            type_path_over = '/'+'/'.join(type_args)
            unr_resource.properties.set('database.category', category_over)
            unr_resource.properties.set('database.type', type_over)
            unr_resource.properties.set('database.type_path', type_path_over)
            unr_resource.properties.set('gui.name', '{}[{}]'.format(resource_name, type_path_over))
        else:
            if 'category' in file_variants:
                category = file_variants['category']
            else:
                category = self._category or 'other'
            if 'type' in file_variants:
                type_ = file_variants['type']
            else:
                type_ = self._type or 'other'

            unr_resource.properties.set('database.category', category)
            unr_resource.properties.set('database.type', type_)

            type_path = '/'+'/'.join([self._category_group, category, type_])
            unr_resource.properties.set('database.type_path', type_path)
            unr_resource.properties.set('gui.name', '{}[{}]'.format(resource_name, type_path))
        unr_resource.properties.set('gui.icon_file', gui_core.GuiIcon.get('database/resource'))
        #
        unr_resource.properties.set('gui.tool_tip', file_variants)
        #
        self.__unr_add_version(unr_resource, version_name, pattern_kwargs, file_variants)

    def __unr_add_version(self, unr_resource, version_name, pattern_kwargs, file_variants):
        version_dtb_path = '{}/{}'.format(unr_resource.get_path(), version_name)
        unr_version = self._unr_version_type.create_obj(version_dtb_path)
        unr_version.properties.set('pattern_kwargs', pattern_kwargs)
        unr_version.properties.set('gui.icon_file', gui_core.GuiIcon.get('database/version'))
        #
        if 'image' in self._options_prx_node.get('includes'):
            self.__unr_add_image_preview(unr_version, file_variants)
        #
        if 'texture' in self._options_prx_node.get('includes'):
            self.__unr_add_textures(unr_version, file_variants)
        #
        if 'hdri' in self._options_prx_node.get('includes'):
            self.__unr_add_hdri(unr_version, file_variants)

    def __unr_add_image_preview(self, unr_version, resource_variants):
        enable = self._options.get('image.preview_enable')
        if enable is True:
            pattern = self._options.get('image.preview.match_patterns')
            matches = self.get_matches_by_patterns(pattern, resource_variants)
            if matches:
                file_variants = matches[0]
                file_path_src = file_variants['result']
                pattern_kwargs = copy.copy(unr_version.properties.get('pattern_kwargs'))
                preview_dtb_path = '{}/image_preview_file'.format(unr_version.get_path())
                unr_preview = self._unr_image_type.create_obj(preview_dtb_path)
                unr_preview.properties.set('pattern_kwargs', pattern_kwargs)
                unr_preview.properties.set('storage.file_src', file_path_src)
                unr_preview.properties.set('gui.icon_file', gui_core.GuiIcon.get('file/resource-preview'))
                unr_preview.properties.set('gui.tool_tip', file_variants)

    def __unr_add_textures(self, unr_version, resource_variants):
        for i_texture_type in self.TEXTURE_KEYS:
            i_enable_key, i_pattern_key = 'texture.{}_enable'.format(
                i_texture_type
                ), 'texture.{}.match_patterns'.format(i_texture_type)
            i_enable = self._options.get(i_enable_key)
            if i_enable is True:
                i_pattern = self._options.get(i_pattern_key)
                i_matches = self.get_matches_by_patterns(i_pattern, resource_variants)
                if i_matches:
                    i_file_variants = i_matches[0]
                    self.__unr_add_texture(unr_version, i_texture_type, i_file_variants)

    def __unr_add_texture(self, unr_version, texture_type_tag, file_variants):
        file_path_src = file_variants['result']
        texture_name = 'texture_{}_file'.format(texture_type_tag)
        pattern_kwargs = copy.copy(unr_version.properties.get('pattern_kwargs'))
        pattern_kwargs['texture_type_tag'] = texture_type_tag
        pattern_kwargs['format'] = file_variants['format']
        texture_dtb_path = '{}/{}'.format(unr_version.get_path(), texture_name)

        unr_texture = self._unr_texture_type.create_obj(texture_dtb_path)
        unr_texture.properties.set('pattern_kwargs', pattern_kwargs)
        unr_texture.properties.set('storage.file_src', file_path_src)
        unr_texture.properties.set('gui.icon_file', gui_core.GuiIcon.get('file/texture'))
        unr_texture.properties.set('gui.tool_tip', file_variants)

    def __unr_add_hdri(self, unr_version, file_variants):
        file_path_src = file_variants['result']
        hdri_name = 'hdri_file'
        pattern_kwargs = copy.copy(unr_version.properties.get('pattern_kwargs'))
        pattern_kwargs['format'] = file_variants['format']
        hdri_dtb_path = '{}/{}'.format(unr_version.get_path(), hdri_name)

        unr_hdri = self._unr_hdri_type.create_obj(hdri_dtb_path)
        unr_hdri.properties.set('pattern_kwargs', pattern_kwargs)
        unr_hdri.properties.set('storage.file_src', file_path_src)
        unr_hdri.properties.set('gui.icon_file', gui_core.GuiIcon.get('file/hdri'))
        unr_hdri.properties.set('gui.tool_tip', file_variants)

    def __unr_add_geometries(self):
        pass

    def __refresh_status(self):
        pass


def main(session):
    import lxgui.proxy.core as gui_prx_core

    gui_prx_core.GuiProxyUtil.show_window_proxy_auto(
        PnlRscTextureAddTool, session=session
    )


if __name__ == '__main__':
    # noinspection PyUnresolvedReferences
    main(session)
