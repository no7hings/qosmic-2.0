# coding:utf-8
import os

python_file_path = '{}/maya-startup.py'.format(
    os.path.dirname(__file__),
)

mel_file_path = '{}/resource-manager.mel'.format(
    os.path.dirname(__file__),
)

with open(python_file_path) as p_f:
    py_script = p_f.read()

py_script += '\n    import lxsession.commands as ssn_commands; ssn_commands.execute_hook(\'*/*/qsm-asset-manager\')\n'

mel_script = 'scriptToShelf "Resource Manager" {} "0";'.format(
    repr(py_script).replace('"', '\"').strip(),

)

print mel_script

with open(mel_file_path, 'w') as m_f:
    m_f.write(mel_script)
