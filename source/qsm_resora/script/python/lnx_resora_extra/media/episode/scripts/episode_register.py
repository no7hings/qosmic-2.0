# coding:utf-8
import lxbasic.log as bsc_log

import lxbasic.core as bsc_core

import lxbasic.scan as bsc_scan

import lxbasic.pinyin as bsc_pinyin

import lxbasic.storage as bsc_storage

import lnx_screw.core as lnx_scr_core

import lxgui.core as gui_core


class EpisodeRegister(object):
    def __init__(
        self,
        scr_stage, file_path,
        with_auto_class, auto_class_file_pattern, auto_class_type_pattern,
        collect_source
    ):
        assert isinstance(scr_stage, lnx_scr_core.Stage)

        self._scr_stage = scr_stage
        self._file_path = file_path

        self._with_auto_class = with_auto_class
        self._auto_class_file_pattern = auto_class_file_pattern
        self._auto_class_type_pattern = auto_class_type_pattern

        self._ignore_exists = True

        self._collect_source = collect_source

    def create_type_fnc(self):
        pass

    def execute(self, scr_type_paths=None, scr_tag_paths=None):
        file_opt = bsc_storage.StgFileOpt(self._file_path)

        file_kwargs = dict(
            file_directory=file_opt.directory_path,
            file_name=file_opt.name_base,
            file_format=file_opt.format,
        )

        file_name = file_opt.name

        uuid = file_opt.to_hash_uuid()

        exist_node = self._scr_stage.find_one(
            entity_type=self._scr_stage.EntityTypes.Node,
            filters=[
                ('uuid', 'is', uuid)
            ]
        )
        if exist_node:
            if self._ignore_exists is True:
                return

            scr_node_path = exist_node.path
        else:
            file_name = file_opt.name

            user = file_opt.get_user()
            ctime = file_opt.get_ctime()
            mtime = file_opt.get_mtime()

            dcc_name = bsc_pinyin.Text.to_dcc_name(file_name)
            index_maximum = self._scr_stage.get_entity_index_maximum(self._scr_stage.EntityTypes.Node)
            scr_node_path = '/{}_{}'.format(dcc_name, index_maximum+1)

            self._scr_stage.create_node(
                scr_node_path,
                gui_name=file_name,
                gui_name_chs=file_name,
                user=user,
                ctime=float(ctime),
                mtime=float(mtime),
                uuid=uuid
            )

        # source
        self._scr_stage.upload_node_video(
            scr_node_path, self._file_path, self._collect_source
        )

        # type assign
        if self._with_auto_class:
            ptn_opt = bsc_core.AbsParseOpt(self._auto_class_file_pattern, file_kwargs)
            type_variants = ptn_opt.get_variants(file_name)
            if type_variants:
                scr_type_path = self._auto_class_type_pattern.format(**type_variants)

                type_components = bsc_core.BscNodePath.get_dag_component_paths(scr_type_path)
                type_components.reverse()
                for i_scr_type_path in type_components[:-1]:
                    i_type_name = bsc_core.BscNodePath.to_dag_name(i_scr_type_path)
                    self._scr_stage.create_type_as_group(
                        i_scr_type_path, gui_name=i_type_name, gui_name_chs=i_type_name,
                    )

                type_name = bsc_core.BscNodePath.to_dag_name(scr_type_path)
                self._scr_stage.create_type(
                    scr_type_path, gui_name=type_name, gui_name_chs=type_name,
                )

                self._scr_stage.create_node_type_assign(
                    scr_node_path, scr_type_path
                )

        # type and tag
        if scr_type_paths:
            [self._scr_stage.create_node_type_assign(scr_node_path, x) for x in scr_type_paths]

        if scr_tag_paths:
            [self._scr_stage.create_node_tag_assign(scr_node_path, x) for x in scr_tag_paths]


class EpisodeRegisterBatch(object):
    @classmethod
    def get_files_fnc(cls, directory_path, file_pattern, file_formats):
        directory_kwargs = dict(
            directory=directory_path
        )

        file_formats = [str(x).strip() for x in file_formats.split(',')]

        set_ = set()

        for i_format in file_formats:
            i_kwargs = dict(directory_kwargs)
            i_kwargs['format'] = i_format

            i_regex = file_pattern.format(
                **i_kwargs
            )

            i_file_paths = bsc_scan.ScanGlob.glob_files(i_regex)

            if i_file_paths:
                set_.update(set(i_file_paths))

        list_ = list(set_)
        list_.sort()
        return list_

    @classmethod
    def register_fnc(
        cls,
        database_name, directory_path,
        file_pattern='{directory}//*.{format}', file_formats='mov, mp4, avi',
        with_auto_class=False, auto_class_file_pattern='{episode}_{sequence}_*.{format}',
        auto_class_type_pattern='/{episode}/{sequence}',
        collect_source=False,
        scr_type_paths=None, scr_tag_paths=None
    ):
        file_paths = cls.get_files_fnc(directory_path, file_pattern, file_formats)

        if file_paths:
            result = gui_core.GuiApplication.exec_message_dialog(
                u'\n'.join(file_paths),
                title='Upload Files',
                size=(480, 480),
                status='warning',
            )
            if result:
                cls(
                    database_name, file_paths, 
                    with_auto_class=with_auto_class, auto_class_file_pattern=auto_class_file_pattern,
                    auto_class_type_pattern=auto_class_type_pattern,
                    collect_source=collect_source
                ).execute(
                    scr_type_paths, scr_tag_paths
                )
        else:
            gui_core.GuiApplication.exec_message_dialog(
                'File is not found.',
                title='Upload Files',
                size=(480, 480),
                status='warning',
            )

    def __init__(
        self, 
        database_name, file_paths,
        with_auto_class, auto_class_file_pattern, auto_class_type_pattern,
        collect_source
    ):
        self._scr_stage = lnx_scr_core.Stage(database_name)
        self._file_paths = file_paths

        self._with_auto_class = with_auto_class
        self._auto_class_file_pattern = auto_class_file_pattern
        self._auto_class_type_pattern = auto_class_type_pattern

        self._collect_source = collect_source

    def execute(self, scr_type_paths=None, scr_tag_paths=None):
        if self._file_paths:
            with bsc_log.LogProcessContext.create(maximum=len(self._file_paths)) as l_p:
                for i_file_path in self._file_paths:
                    # noinspection PyBroadException
                    try:
                        EpisodeRegister(
                            self._scr_stage, i_file_path,
                            self._with_auto_class, self._auto_class_file_pattern, self._auto_class_type_pattern,
                            self._collect_source
                        ).execute(scr_type_paths, scr_tag_paths)
                    except Exception:
                        pass
                    finally:
                        l_p.do_update()

