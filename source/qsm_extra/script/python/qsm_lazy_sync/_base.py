# coding:utf-8
import os

import enum

import json

import uuid

import time


class SyncBase(object):
    class Status(enum.IntEnum):
        Unknown = 0
        Started = 1
        Running = 2
        Waiting = 3
        Completed = 4
        Suspended = 5
        Failed = 6
        Stopped = 7
        Error = 8
        Killed = 9
        Finished = 10

    LOCATION = 'Z:/caches/database/sync-task/tasks'

    DATE_TAG_FORMAT = '%Y_%m%d'

    @classmethod
    def _read_json(cls, json_path):
        with open(json_path) as j:
            # noinspection PyTypeChecker
            raw = json.load(j)
            j.close()
            return raw

    @classmethod
    def _write_json(cls, json_path, data):
        dir_path = os.path.dirname(json_path)
        if os.path.exists(dir_path) is False:
            os.makedirs(dir_path)

        with open(json_path, 'w') as j:
            json.dump(
                data,
                j,
                indent=4
            )

    @classmethod
    def _generate_date_tag(cls):
        timestamp = time.time()
        return time.strftime(
            cls.DATE_TAG_FORMAT,
            time.localtime(timestamp)
        )

    @classmethod
    def _generate_task_id(cls):
        return str(uuid.uuid1()).upper()

    @classmethod
    def _generate_task_json_path(cls, task_id):
        return '{}/{}.json'.format(
            cls.LOCATION,
            task_id
        )

    @classmethod
    def _generate_cmd_script(cls, json_path):
        main_arg = 'rez-env qsm_main'
        cmd_args = [
            main_arg,
            '-- qsm-hook-json -j "{}"'.format(json_path)
        ]
        return ' '.join(cmd_args)
