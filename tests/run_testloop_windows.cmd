@echo off
set ERR_TXT_MYPY=[91m ************************************** ERROR in MYPY **************************************[0m
set ERR_TXT_PYTEST=[91m ************************************** ERROR in PYTEST **************************************[0m
set sleeptime_on_error=3

:loop
    pytest --pep8
    if  %errorlevel% gtr 0 (
        echo %ERR_TXT_PYTEST%
        call:function_beep
        call:function_sleep %sleeptime_on_error%
    )

    mypy %CD% --strict --no-warn-unused-ignores
    if  %errorlevel% gtr 0 (
        echo %ERR_TXT_MYPY%
        call:function_beep
        call:function_sleep %sleeptime_on_error%
    )
goto loop



:function_sleep
    REM %~1 : Time in seconds to wait
    set sleep_seconds=%~1
    set /A sleep_milliseconds = %sleep_seconds% * 1000
    ping 192.0.2.2 -n 1 -w %sleep_milliseconds% > nul
GOTO:EOF

:function_beep
    @echo 
GOTO:EOF