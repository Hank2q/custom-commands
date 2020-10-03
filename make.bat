@echo off
if %1==webpage (CALL :Make index.html & CALL :Make style.css & CALL :Make app.js & EXIT /B 0) else (CALL :Make %1 & EXIT /B 0)

:Make
echo File: [%~1] created 2> %~1

