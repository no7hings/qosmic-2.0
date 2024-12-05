# coding:utf-8
import _my_sql

import re

import _abc

import _handle


class Stage(_abc.AbsBase):

    def __init__(self):
        pass

    def create_project(self, name, **kwargs):
        project = _handle.Database(name)
        project.build(**kwargs)

    def get_project(self, name):
        database_name = self._to_project_database_name(name)
        if _my_sql.MySql.database_is_exists(
            self._get_mysql_options(), database_name
        ) is True:
            return _handle.Database(name).find_one(
                self.EntityTypes.Project,
                [
                    ('name', 'is', name)
                ]
            )

    def find_all_projects(self):
        list_ = []
        database_names = _my_sql.MySql.get_all_database_names(
            self._get_mysql_options()
        )
        ptn = r'{}_(.*)'.format(self.DATABASE_ROOT_NAME)
        for i_name in database_names:
            if re.match(ptn, i_name, re.DOTALL):
                i_r = re.search(ptn, i_name, re.DOTALL)
                i_name = i_r.group(1)
                i_project = self.get_project(name=i_name)
                if i_project:
                    list_.append(i_project)
        return list_

    def create_role(self, name, **kwargs):
        pass

    def create_asset(self, name, **kwargs):
        pass

    def create_episode(self, name, **kwargs):
        pass

    def create_sequence(self, name, **kwargs):
        pass

    def create_shot(self, name, **kwargs):
        pass
