@echo off
pushd %~d0
set QSM_PYTHON_VERSION=3
set PYTHONPATH=%PYTHONPATH%;C:\Users\nothings\AppData\Local\Programs\Python\Python310\Lib\site-packages
rez-env qsm_main pyside2-5.15.2 ffmpeg -- qsm-hook-python -o "hook_key=desktop-tools/desktop-tool-kit"
popd
