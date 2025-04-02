# coding:utf-8
import re

from . import _my_sql

from . import _abc_

from . import _handle


class Stage(_abc_.AbsBase):

    def __init__(self):
        pass

    def initialize(self):
        database = _handle.Database(self.EntityTypes.User, 'master')
        database.initialize()

    def create_user(self, name, **kwargs):
        pass

    def create_project(self, name, **kwargs):
        database = _handle.Database(self.EntityTypes.Project, name)
        database.build(**kwargs)

    def get_project(self, name):
        database_name = self._to_database_key(self.EntityTypes.Project, name)
        if _my_sql.MySql.database_is_exists(
            self._get_mysql_options(), database_name
        ) is True:
            return _handle.Database(self.EntityTypes.Project, name).find_one(
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
        ptn = r'{}_{}_(.*)'.format(self.DATABASE_ROOT_NAME, self.EntityTypes.Project)
        for i_name in database_names:
            if re.match(ptn, i_name, re.IGNORECASE):
                i_r = re.search(ptn, i_name, re.IGNORECASE)
                i_name = i_r.group(1)
                i_project = self.get_project(name=i_name)
                if i_project:
                    list_.append(i_project)
        return list_
