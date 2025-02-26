if "%QSM_PYTHON_VERSION%"=="3" (
    set QSM_BIN_PYTHON=%QSM_LIB_BASE%\bin\windows-python-3.10\python
) else (
    set QSM_BIN_PYTHON=%QSM_LIB_BASE%\bin\windows-python-2.7.18\python
)

%QSM_BIN_PYTHON% %QSM_CORE_BASE%\script\bin\python\qsm-hook-server.py %*