if "%QSM_PYTHON_VERSION%"=="3" (
    set PATH=%PATH%;%QSM_LIB_BASE%\bin\windows-python-3.10
    set PATH=%PATH%;%QSM_LIB_BASE%\bin\windows-x64-python-3.10\Scripts
    set QSM_BIN_PYTHON=%QSM_LIB_BASE%\bin\windows-python-3.10\python
) else (
    set PATH=%PATH%;%QSM_LIB_BASE%\bin\windows-python-2.7.18
    set PATH=%PATH%;%QSM_LIB_BASE%\bin\windows-x64-python-2.7.18\Scripts
    set QSM_BIN_PYTHON=%QSM_LIB_BASE%\bin\windows-python-2.7.18\python
)

%QSM_BIN_PYTHON% %*