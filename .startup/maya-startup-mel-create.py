# coding:utf-8
import os

tool_names = [
    ('qsm-asset-manager', 'Resource Manager'),
    ('qsm-easy-playblast', 'Easy Playblast'),
]

python_file_path = '{}/maya-startup.py'.format(
    os.path.dirname(__file__),
)

for i_key, i_name in tool_names:
    mel_file_path = '{}/maya/{}.mel'.format(
        os.path.dirname(__file__), i_key
    )

    with open(python_file_path) as p_f:
        py_script = p_f.read()

    py_script += '\n    import lxsession.commands as ssn_commands; ssn_commands.execute_hook(\'*/*/{}\')\n'.format(i_key)

    mel_script = 'scriptToShelf "{}" {} "0";'.format(
        i_name, repr(py_script).replace('"', '\"').strip(),
    )

    with open(mel_file_path, 'w') as m_f:
        m_f.write(mel_script)
