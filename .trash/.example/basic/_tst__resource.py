# coding:utf-8
import lxbasic.resource as bsc_resource

import lxbasic.core as bsc_core

file_path = bsc_resource.ExtendResource.get('scripts/any-file-to-clarisse.py')

bsc_core.BscScriptExecute.execute_python_file(
    file_path, options=dict(location='/test', file='/test')
)

