# coding:utf-8
from __future__ import print_function

import os

import shutil

import requests

from . import _base

from . import _url

from . import _configure


class TaskClient(object):

    @classmethod
    def new_task(cls, fnc, *args, **kwargs):
        url = 'http://{host}:{port}/task_new'.format(
            host=_configure.SyncServer.HOST, port=_configure.SyncServer.PORT
        )

        options = dict(
            fnc=fnc,
            args=args,
            kwargs=kwargs
        )

        task_id = _base.SyncBase._generate_task_id()
        json_path = _base.SyncBase._generate_task_json_path(task_id)
        _base.SyncBase._write_json(json_path, options)

        data = dict(
            json=json_path
        )

        headers = {'Content-Type': 'application/json'}
        return _url.UrlFnc.send_async_request(url, data, headers)

    @classmethod
    def restart_task(cls, json_path):
        url = 'http://{host}:{port}/task_new'.format(
            host=_configure.SyncServer.HOST, port=_configure.SyncServer.PORT
        )

        data = dict(
            json=json_path
        )

        headers = {'Content-Type': 'application/json'}
        return _url.UrlFnc.send_async_request(url, data, headers)

    @classmethod
    def requeue_tasks(cls):
        list_ = []
        location = _base.SyncBase.LOCATION
        keys = os.listdir(location)
        for i_key in keys:
            i_path = '{}/{}'.format(location, i_key)
            if os.path.isfile(i_path) and i_path.endswith('.json'):
                list_.append(i_path)
            elif os.path.isdir(i_path):
                if i_key in [
                    '.running',
                    # ignore waiting
                    # '.waiting',
                    '.failed',
                    '.error'
                ]:
                    i_keys = os.listdir(i_path)
                    for j_key in i_keys:
                        j_path = '{}/{}'.format(i_path, j_key)
                        if os.path.isfile(j_path) and j_path.endswith('.json'):
                            j_basename = os.path.basename(j_path)
                            j_path_new = '{}/{}'.format(location, j_basename)
                            shutil.move(j_path, j_path_new)
                            list_.append(j_path_new)

        for i_json_path in list_:
            cls.restart_task(i_json_path)

    @classmethod
    def check_status(cls):
        url = 'http://{host}:{port}/server_status'.format(
            host=_configure.SyncServer.HOST, port=_configure.SyncServer.PORT
        )
        try:
            response = requests.get(url)
            if response.status_code == 200:
                _ = response.json()
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            return False
