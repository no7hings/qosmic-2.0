# coding:utf-8
import time

import json

import subprocess

import lxbasic.core as bsc_core

import lxbasic.crypto.core as bsc_cpt_core

data_dict = dict(
    password='admin',
    timestamp=time.time()
)

# cmd_args = [
#     r'rez-env qsm_main -- qsm-crypto -e -k QOSMIC -j "{\"name\": \"example\", \"verbose\": true, \"output\": \"file.txt\"}"'
# ]
#
# cmd_script = ' '.join(cmd_args)
# result = subprocess.Popen(cmd_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
# stdout, stderr = result.communicate()
#
# if result.returncode != 0:
#     print('AAA')

bsc_core.BscProcess.execute_as_trace(
    r'rez-env qsm_main -- qsm-crypto -e -k "{}" -j "{}"'.format(
        'QOSMIC',
        json.dumps(data_dict).replace('"', '\\"')
    )
)

bsc_core.BscProcess.execute_as_trace(
    r'rez-env qsm_main -- qsm-crypto -d -k "{}" -j "{}"'.format(
        'QOSMIC',
        '{"data": "3I6KtUIYcx/UJcfUFjPTyiPeg6UHkgWm73ZM4AErM+YbtZscB8J+wvHFtsbsPXPe3Um96uUw73b2ozvhW2JtqQ==", "iv": "ryiIw2gS/ROLNFWAUpDzBg=="}'.replace('"', '\\"')
    )
)
