# coding:utf-8
from __future__ import print_function

import sys

import threading

import flask

import multiprocessing

import lxbasic.log as bsc_log

import lxbasic.storage as bsc_storage

import qsm_task_pool.core as qsm_tsk_pol_core

from . import base as _base

argv = sys.argv

APP = flask.Flask(__name__)


class HookServer(object):
    @classmethod
    def error(cls):
        pass

    @classmethod
    def warning(cls):
        pass

    @classmethod
    def result(cls):
        pass

    @staticmethod
    @APP.route("/test")
    def test_fnc():
        return 'Hello world'

    @staticmethod
    @APP.route("/query")
    def query_fnc():
        options = flask.request.args
        response = {
            'status': 'started'
        }
        return flask.jsonify(
            response
        )

    @staticmethod
    @APP.route("/task")
    def task_fnc():
        p = qsm_tsk_pol_core.Pool.generate()

        options = flask.request.args

        unique_id = options.get('uuid')
        if unique_id:
            hook_file_path = _base.HookBase.get_file_path(uuid=unique_id)
            hook_yml_file = bsc_storage.StgFileOpt(hook_file_path)
            if hook_yml_file.get_is_exists() is True:
                raw = hook_yml_file.set_read()
                if raw:
                    group = raw.get('group')
                    name = raw.get('name')
                    cmd_script = raw.get('cmd_script')
                    completion_notice = raw.get('completion_notice')

                    task = p.new_task(
                        group=group,
                        name=name,
                        cmd_script=cmd_script,
                        completion_notice=completion_notice,
                    )
                    # use thread
                    t = threading.Thread(
                        target=task.do_wait_for_start
                    )
                    t.setDaemon(True)
                    t.start()

                    response = dict(
                        result=dict(
                            task_id=task.task_id
                        )
                    )

                    return flask.jsonify(response)
            else:
                bsc_log.Log.trace_method_warning(
                    'hook',
                    'key="{}" is non-exists'.format(hook_file_path)
                )

        response = dict(
            result=dict(
                uuid=unique_id
            )
        )
        return flask.jsonify(response)


def start_server():
    APP.run(host="0.0.0.0", debug=1, port=9527, use_reloader=False)


def start_server_process():
    flask_process = multiprocessing.Process(target=start_server)
    flask_process.start()
    return flask_process


if __name__ == '__main__':
    start_server()
