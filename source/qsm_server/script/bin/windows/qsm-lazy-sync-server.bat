@echo off

:: Check for admin rights
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator privileges...
    powershell -Command "Start-Process '%~0' -Verb RunAs"
    exit /b
)

subst X: "E:\myworkspace\map_x"
subst Y: "E:\myworkspace\pipeline-root"
subst Z: "E:\myworkspace\production-root"

set QSM_SERVER_BASE=E:/myworkspace/qosmic-2.0/source/qsm_server
set QSM_SYNC_TASK_ROOT=Z:/caches/database/sync-task/tasks
set QSM_PYTHON=Y:/deploy/.python/windows/2.7.18/python.exe

set PYTHONPATH=%PYTHONPATH%;%QSM_SERVER_BASE%/lib/python-2.7;%QSM_SERVER_BASE%/lib/windows-python-2.7;%QSM_SERVER_BASE%/script/python

%QSM_PYTHON% %QSM_SERVER_BASE%\script\bin\python\qsm-lazy-sync-server.py %*

popd

pause
