# coding:utf-8
import copy

import lxbasic.core as bsc_core
# qt
from ....qt import core as _qt_core
# qt widgets
from ....qt.widgets.input import input_for_bubble as _qt_wgt_ipt_for_bubble

from ....qt.widgets.input import input_for_entity as _qt_wgt_ipt_for_path

from ....qt.widgets import base as _qt_wgt_base

from ....qt.widgets import utility as _qt_wgt_utility
# proxy abstracts
from ... import abstracts as _prx_abstracts


class PrxInputAsStgTask(_prx_abstracts.AbsPrxWidget):
    QT_WIDGET_CLS = _qt_wgt_utility.QtTranslucentWidget
    
    class Schemes(object):
        AssetTask = 'asset-task'

        SequenceTask = 'sequence-task'
        ShotTask = 'shot-task'

        ProjectTask = 'project-task'

        All = [
            AssetTask,
            SequenceTask,
            ShotTask,
            ProjectTask
        ]

    def __init__(self, *args, **kwargs):
        super(PrxInputAsStgTask, self).__init__(*args, **kwargs)

        self.__signals = _qt_core.QtActionSignals(self.get_widget())

        self.__resource_type = 'asset'
        self.__scheme = self.Schemes.AssetTask

        self.__next_tip = '...'

        self.__project_dict = {}
        self.__resource_dict = {}
        self.__task_dict = {}

        self.__stg_task = None
        self.__result_dict = {}

        import lxbasic.shotgun as bsc_shotgun

        self._stg_connector = bsc_shotgun.StgConnector()

        l_0 = _qt_wgt_base.QtHBoxLayout(self.get_widget())
        l_0.setContentsMargins(*[0]*4)
        l_0._set_align_as_top_()

        self._qt_scheme_input = _qt_wgt_ipt_for_bubble.QtInputForBubbleChoose()
        l_0.addWidget(self._qt_scheme_input)
        self._qt_scheme_input._set_choose_values_(
            self.Schemes.All
        )
        self._qt_scheme_input.input_value_accepted.connect(
            self.__update_branch
        )

        self._qt_entity_input = _qt_wgt_ipt_for_path.QtInputForEntity()
        l_0.addWidget(self._qt_entity_input)

        self._qt_entity_input._set_next_buffer_fnc_(
            self._next_buffer_fnc
        )

        self._qt_entity_input._set_value_('/')

        self._qt_entity_input._setup_()

        self._qt_entity_input.input_value_accepted.connect(self.__update_task)
        self._qt_entity_input.user_input_entry_finished.connect(self.__accept_result)

        self._qt_scheme_input._set_value_(self.Schemes.AssetTask)

        self._qt_scheme_input._set_history_key_('gui.shotgun-branch')
        self._qt_scheme_input._pull_history_()

        self._qt_entity_input._set_history_key_('gui.input-path-{}'.format(self.__scheme))
        self._qt_entity_input._pull_history_()

        self._qt_entity_input._create_widget_shortcut_action_(
            self.__to_next_scheme, 'Alt+Right'
        )
        self._qt_entity_input._create_widget_shortcut_action_(
            self.__to_previous_scheme, 'Alt+Left'
        )

    def __to_next_scheme(self):
        self._qt_scheme_input._get_entry_widget_()._to_next_()

    def __to_previous_scheme(self):
        self._qt_scheme_input._get_entry_widget_()._to_previous_()

    def set_focus_in(self):
        self._qt_entity_input._set_input_entry_focus_in_()

    def has_focus(self):
        return self._qt_entity_input._get_input_entry_has_focus_()

    def connect_result_to(self, fnc):
        self.__signals.dict_accepted.connect(fnc)

    def connect_tip_trace_to(self, fnc):
        self.__signals.str_accepted.connect(fnc)

    def __update_branch(self, text):
        if text != self.__scheme:
            path_text = self._qt_entity_input._get_value_()
            path = bsc_core.BscNodePathOpt(path_text)

            self.__scheme = text
            self._qt_entity_input._restore_next_cache_()

            self.__resource_type = None
            if self.__scheme == self.Schemes.AssetTask:
                self.__resource_type = 'asset'
            elif self.__scheme == self.Schemes.SequenceTask:
                self.__resource_type = 'sequence'
            elif self.__scheme == self.Schemes.ShotTask:
                self.__resource_type = 'shot'

            self._qt_entity_input._set_history_key_('gui.input-path-{}'.format(self.__scheme))
            if self._qt_entity_input._pull_history_() is False:
                cs = path.get_components()
                cs.reverse()
                d = len(cs)
                if d > 1:
                    self._qt_entity_input._set_value_(cs[1].to_string())

            path_text_cur = self._qt_entity_input._get_value_()
            if path_text_cur == path_text:
                self._qt_entity_input._update_next_()

    def _cache_projects(self):
        self.__project_dict = {}
        (
            self.__project_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict
        ) = self._stg_connector.generate_stg_gui_args(
            shotgun_entity_kwargs=dict(
                entity_type='Project',
                filters=[
                    ['users', 'in', [self._stg_connector.get_current_stg_user()]],
                    ['sg_status', 'in', ['Active', 'Accomplish']]
                ],
                fields=['name', 'sg_description']
            ),
            name_field='name',
            keyword_filter_fields=['name', 'sg_description'],
            tag_filter_fields=['sg_status']
        )
        return self.__project_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict

    def _cache_resources(self, project):
        self.__resource_type = None
        if self.__scheme == self.Schemes.AssetTask:
            self.__resource_type = 'asset'
            stg_entity_type = self._stg_connector.StgEntityTypes.Asset
            tag_filter_fields = ['sg_asset_type']
            keyword_filter_fields = ['code', 'sg_chinese_name']
        elif self.__scheme == self.Schemes.SequenceTask:
            self.__resource_type = 'sequence'
            stg_entity_type = self._stg_connector.StgEntityTypes.Sequence
            tag_filter_fields = ['tags']
            keyword_filter_fields = ['code', 'description']
        elif self.__scheme == self.Schemes.ShotTask:
            self.__resource_type = 'shot'
            stg_entity_type = self._stg_connector.StgEntityTypes.Shot
            tag_filter_fields = ['sg_sequence']
            keyword_filter_fields = ['code', 'description']
        else:
            raise RuntimeError()

        (
            self.__resource_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict
        ) = self._stg_connector.generate_stg_gui_args(
            shotgun_entity_kwargs=dict(
                entity_type=stg_entity_type,
                filters=[
                    ['project', 'is', self._stg_connector.get_stg_project(project=project)],
                ],
                fields=keyword_filter_fields
            ),
            name_field='code',
            keyword_filter_fields=keyword_filter_fields,
            tag_filter_fields=tag_filter_fields,
        )
        return self.__resource_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict

    def _cache_project_tasks(self, project):
        kw = {
            'project': project,
        }
        (
            self.__task_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict
        ) = self._stg_connector.generate_stg_gui_args(
            shotgun_entity_kwargs={
                'entity_type': 'Task',
                'filters': [
                    ['entity', 'is', self._stg_connector.get_stg_project(**kw)]
                ],
                'fields': ['content', 'sg_status_list'],
            },
            name_field='content',
            keyword_filter_fields=['content', 'sg_status_list'],
            tag_filter_fields=['step'],
        )
        return self.__task_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict

    def _cache_resource_tasks(self, project, resource):
        kw = {
            'project': project,
            self.__resource_type: resource
        }
        (
            self.__task_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict
        ) = self._stg_connector.generate_stg_gui_args(
            shotgun_entity_kwargs={
                'entity_type': 'Task',
                'filters': [
                    ['entity', 'is', self._stg_connector.get_stg_resource(**kw)]
                ],
                'fields': ['content', 'sg_status_list'],
            },
            name_field='content',
            keyword_filter_fields=['content', 'sg_status_list'],
            tag_filter_fields=['step'],
        )
        return self.__task_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict

    def __update_project_task_result(self, project, task):
        kw = {
            'project': project,
            'task': task
        }
        self.__stg_task = self._stg_connector.find_stg_task(
            **kw
        )
        if self.__stg_task:
            result = copy.copy(kw)
            result['scheme'] = self.__scheme
            result['project'] = kw['project'].lower()
            result['branch'] = self.__resource_type
            result['task_id'] = self.__stg_task['id']
            self.__result_dict = result
            return True
        return False

    def __update_resource_task_result(self, project, resource, task):
        kw = {
            'project': project,
            self.__resource_type: resource,
            'task': task
        }
        self.__stg_task = self._stg_connector.find_stg_task(
            **kw
        )
        if self.__stg_task:
            result = copy.copy(kw)
            result['scheme'] = self.__scheme
            result['project'] = kw['project'].lower()
            result['branch'] = self.__resource_type
            result['task_id'] = self.__stg_task['id']
            self.__result_dict = result
            return True
        return False

    def __update_task(self, path_text):
        self.__stg_task = None
        self.__result_dict = {}

        if path_text:
            path = bsc_core.BscNodePathOpt(path_text)
            cs = path.get_components()
            cs.reverse()

            self.__next_tip = '...'
            if len(cs) == 1:
                self.__next_tip = 'enter or choose a "project"'
            elif len(cs) == 2:
                if self.__scheme == self.Schemes.ProjectTask:
                    self.__next_tip = 'enter or choose a "task"'
                else:
                    self.__next_tip = 'enter or choose a "{}"'.format(self.__scheme)
            elif len(cs) == 3:
                if self.__scheme == self.Schemes.ProjectTask:
                    project = cs[1].get_name()
                    task = cs[2].get_name()
                    result = self.__update_project_task_result(project, task)
                    if result is True:
                        self.__next_tip = 'task id is "{}", press "Enter" to accept'.format(
                            self.__result_dict['task_id']
                        )
                    else:
                        self.__next_tip = 'task is not valid'
                else:
                    self.__next_tip = 'enter or choose a "task"'
            elif len(cs) == 4:
                project = cs[1].get_name()
                resource = cs[2].get_name()
                task = cs[3].get_name()
                result = self.__update_resource_task_result(project, resource, task)
                if result is True:
                    self.__next_tip = 'task id is "{}", press "Enter" to accept'.format(
                        self.__result_dict['task_id']
                    )
                else:
                    self.__next_tip = 'task is not valid'

            self.__accept_tip()

    def _next_buffer_fnc(self, path):
        dict_ = {}

        cs = path.get_components()
        cs.reverse()
        d = len(cs)
        if d == 1:
            (
                entity_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict
            ) = self._cache_projects()
        elif d == 2:
            project = cs[1].get_name()
            if self.__scheme == self.Schemes.ProjectTask:
                (
                    entity_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict
                ) = self._cache_project_tasks(project)
            else:
                (
                    entity_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict
                ) = self._cache_resources(project)
        elif d == 3:
            if self.__scheme == self.Schemes.ProjectTask:
                entity_dict = {}
                name_texts = []
                image_url_dict = {}
                keyword_filter_dict = {}
                tag_filter_dict = {}
            else:
                project = cs[1].get_name()
                resource = cs[2].get_name()
                (
                    entity_dict, name_texts, image_url_dict, keyword_filter_dict, tag_filter_dict
                ) = self._cache_resource_tasks(project, resource)
        else:
            entity_dict = {}
            name_texts = []
            image_url_dict = {}
            keyword_filter_dict = {}
            tag_filter_dict = {}

        dict_['query_dict'] = entity_dict
        dict_['name_texts'] = name_texts
        dict_['image_url_dict'] = image_url_dict
        dict_['keyword_filter_dict'] = keyword_filter_dict
        dict_['tag_filter_dict'] = tag_filter_dict

        return dict_

    def __accept_result(self):
        self.__update_task(
            self._qt_entity_input._get_value_()
        )
        dict_ = self.__result_dict
        if dict_:
            self.__signals.dict_accepted.emit(dict_)

    def is_valid(self):
        return bool(self.__result_dict)

    def get_result(self):
        return self.__result_dict

    def get_stg_task(self):
        return self.__stg_task

    def __accept_tip(self):
        self.__signals.str_accepted.emit(
            (
                'load task for {}:\n'
                '    press "Alt+Left" or "Alt+Right" to switch branch;\n'
                '    {}.'
            ).format(
                self.__scheme, self.__next_tip
            )
        )

    def get_scheme(self):
        return self.__scheme

    def setup(self):
        self.__accept_tip()

    def setup_from_task_id(self, task_id):
        task_data = self._stg_connector.get_data_from_task_id(
            str(task_id)
        )
        branch = task_data['branch']
        if branch == 'project':
            self._qt_scheme_input._set_value_(
                self.Schemes.ProjectTask
            )
            peth_text = '/{}/{}'.format(task_data['project'], task_data['task'])
        elif branch == 'asset':
            self._qt_scheme_input._set_value_(
                self.Schemes.AssetTask
            )
            peth_text = '/{}/{}/{}'.format(task_data['project'], task_data['asset'], task_data['task'])
        elif branch == 'sequence':
            self._qt_scheme_input._set_value_(
                self.Schemes.SequenceTask
            )
            peth_text = '/{}/{}/{}'.format(task_data['project'], task_data['sequence'], task_data['task'])
        elif branch == 'shot':
            self._qt_scheme_input._set_value_(
                self.Schemes.ShotTask
            )
            peth_text = '/{}/{}/{}'.format(task_data['project'], task_data['shot'], task_data['task'])
        else:
            raise RuntimeError()

        self._qt_entity_input._set_value_(peth_text)
