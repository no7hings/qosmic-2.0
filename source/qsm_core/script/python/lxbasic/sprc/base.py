# coding:utf-8
import os

import subprocess


class SprcUsage(object):
    @classmethod
    def get_cpu(cls, pid):
        command = 'wmic path Win32_PerfFormattedData_PerfProc_Process where IDProcess={} get PercentProcessorTime'.format(
            pid)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output, _ = process.communicate()

        for line in output.splitlines():
            if line.strip().isdigit():
                return float(line.strip())
        return None

    @classmethod
    def get_memory(cls, pid):
        """
        use kb
        """
        tasklist_output = subprocess.check_output(['tasklist', '/FI', 'PID eq {}'.format(pid)])
        for i_line in tasklist_output.splitlines():
            if str(pid) in i_line:
                i_parts = i_line.split()
                i_memory_usage_str = i_parts[-2].replace(',', '')
                return int(i_memory_usage_str)*1024
        return 0


class Subprocess(object):
    @classmethod
    def kill(cls, pid):
        result = subprocess.check_output(
            ["taskkill", "/F", "/T", "/PID", str(pid)],
            shell=True,
            stderr=subprocess.STDOUT
        )
        print result


class SprcDag(object):

    @classmethod
    def get_child_pids(cls, pid):
        cmd_script = 'wmic process where (ParentProcessId={}) get ProcessId'.format(pid)
        process = subprocess.Popen(cmd_script, stdout=subprocess.PIPE, shell=True)
        output, _ = process.communicate()

        list_ = []
        for i_line in output.splitlines():
            i_line = i_line.strip()
            if i_line.isdigit():
                list_.append(int(i_line))

        return list_

    @classmethod
    def get_child_args(cls, pid):
        list_ = []

        cmd_script = 'wmic process where (ParentProcessId={}) get Name,ProcessId'.format(pid)
        output = subprocess.check_output(
            cmd_script
        )
        for i_line in output.splitlines():
            i_parts = i_line.strip().split()
            if len(i_parts) == 2 and i_parts[1].isdigit():
                i_name = i_parts[0]
                i_pid = int(i_parts[1])
                list_.append((i_name, i_pid))

        return list_

    @classmethod
    def get_descendant_args(cls, pid):
        def rcs_fnc_(pid_, indent_):
            indent_ += 4
            for _i_args in cls.get_child_args(pid_):
                _i_name, _i_pid = _i_args
                list_.append((_i_name, _i_pid))
                rcs_fnc_(_i_pid, indent_)

        indent = 0
        list_ = []

        rcs_fnc_(pid, indent)
        return list_

