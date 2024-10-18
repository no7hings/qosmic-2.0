# coding:utf-8
from __future__ import print_function

import requests

import json

import threading

from . import base as _base


class TaskProcessClient(object):

    @classmethod
    def get_server_status(cls):
        url = 'http://{host}:{port}/server_status'.format(
            host=_base.TaskProcessServerBase.HOST, port=_base.TaskProcessServerBase.PORT
        )
        try:
            response = requests.get(url)
            if response.status_code == 200:
                _ = response.json()
                # print('Status Code:', response.status_code)
                # print('Response JSON:', response.json())
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            return False

    @classmethod
    def get_worker_status(cls):
        url = 'http://{host}:{port}/worker_status'.format(
            host=_base.TaskProcessServerBase.HOST, port=_base.TaskProcessServerBase.PORT
        )
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # print('Status Code:', response.status_code)
                # print('Response JSON:', response.json())
                return response.json()
            else:
                return dict(
                    maximum=1,
                    value=0
                )
        except requests.exceptions.RequestException:
            return dict(
                maximum=1,
                value=0
            )

    @classmethod
    def get_worker_queue(cls):
        url = 'http://{host}:{port}/worker_queue'.format(
            host=_base.TaskProcessServerBase.HOST, port=_base.TaskProcessServerBase.PORT
        )
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # print('Status Code:', response.status_code)
                # print('Response JSON:', response.json())
                return response.json()
            else:
                return dict(
                    waiting=[],
                    running=[]
                )
        except requests.exceptions.RequestException:
            return dict(
                waiting=[],
                running=[]
            )

    @classmethod
    def set_worker_maximum(cls, maximum, **kwargs):
        url = 'http://{host}:{port}/worker_maximum'.format(
            host=_base.TaskProcessServerBase.HOST, port=_base.TaskProcessServerBase.PORT
        )

        data = {
            'maximum': maximum
        }
        data.update(**kwargs)

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # print('Status Code:', response.status_code)
        # print('Response JSON:', response.json())
        return response.status_code, response.json()

    @classmethod
    def new_entity(cls, cmd_script, **kwargs):
        url = 'http://{host}:{port}/task_new'.format(
            host=_base.TaskProcessServerBase.HOST, port=_base.TaskProcessServerBase.PORT
        )

        data = {
            'cmd_script': cmd_script
        }
        data.update(**kwargs)

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # print('Status Code:', response.status_code)
        # print('Response JSON:', response.json())
        return response.status_code, response.json()

    @classmethod
    def requeue_task(cls, task_id, **kwargs):
        url = 'http://{host}:{port}/task_requeue'.format(
            host=_base.TaskProcessServerBase.HOST, port=_base.TaskProcessServerBase.PORT
        )

        data = {
            'task_id': task_id
        }
        data.update(**kwargs)

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response:
            # print('Status Code:', response.status_code)
            # print('Response JSON:', response.json())
            return response.status_code, response.json()

    @classmethod
    def requeue_tasks(cls, task_ids, **kwargs):
        url = 'http://{host}:{port}/task_requeue'.format(
            host=_base.TaskProcessServerBase.HOST, port=_base.TaskProcessServerBase.PORT
        )
        data_list = []
        for i_task_id in task_ids:
            i_data = {
                'task_id': i_task_id
            }
            i_data.update(**kwargs)
            data_list.append(i_data)

        headers = {'Content-Type': 'application/json'}
        run_async_requests(url, data_list, headers)

    @classmethod
    def stop_task(cls, task_id, **kwargs):
        url = 'http://{host}:{port}/task_stop'.format(
            host=_base.TaskProcessServerBase.HOST, port=_base.TaskProcessServerBase.PORT
        )

        data = {
            'task_id': task_id
        }
        data.update(**kwargs)

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response:
            # print('Status Code:', response.status_code)
            # print('Response JSON:', response.json())
            return response.status_code, response.json()

    @classmethod
    def stop_tasks(cls, task_ids, **kwargs):
        url = 'http://{host}:{port}/task_stop'.format(
            host=_base.TaskProcessServerBase.HOST, port=_base.TaskProcessServerBase.PORT
        )
        data_list = []
        for i_task_id in task_ids:
            i_data = {
                'task_id': i_task_id
            }
            i_data.update(**kwargs)
            data_list.append(i_data)

        headers = {'Content-Type': 'application/json'}
        run_async_requests(url, data_list, headers)


def send_request(url, data, headers, results):
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        results.append((response.status_code, response.json()))
    except requests.exceptions.RequestException as e:
        results.append(str(e))


def run_async_request(url, data, headers):
    results = []

    thread = threading.Thread(target=send_request, args=(url, data, headers, results))
    thread.start()
    thread.join()

    return results[0]


def run_async_requests(url, data_list, headers):
    results = []
    threads = []

    for data in data_list:
        thread = threading.Thread(target=send_request, args=(url, data, headers, results))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return results
