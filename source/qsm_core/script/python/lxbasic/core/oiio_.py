# coding:utf-8
import six

import subprocess

from ..wrap import *

from . import execute as _execute


class BscOiioImage:
    @classmethod
    def convert(cls, image_path_0, image_path_1):
        image_path_0 = ensure_unicode(image_path_0)
        image_path_1 = ensure_unicode(image_path_1)

        cmd_args = [
            _execute.BscBinExecute.oiiotool(),
            '"{}"'.format(image_path_0),
            '-o', '"{}"'.format(image_path_1),
        ]

        cmd_args = [cmd.encode('mbcs') if isinstance(cmd, six.text_type) else cmd for cmd in cmd_args]

        cmd_script = ' '.join(cmd_args)
        print(cmd_script)
        s_p = subprocess.Popen(cmd_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        s_p.communicate()
