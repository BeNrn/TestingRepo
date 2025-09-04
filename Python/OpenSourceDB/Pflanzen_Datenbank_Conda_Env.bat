rem set path to conda installation and define env name
for /f "delims=" %%i in ('conda info --base') do set CONDAPATH=%%i
set ENVNAME=generalRepo

rem concat the environment path
if %ENVNAME%==base (set ENVPATH=%CONDAPATH%) else (set ENVPATH=%CONDAPATH%\envs\%ENVNAME%)

rem Activate conda env. Call is necessary when activate or deactivate is used
call %CONDAPATH%\Scripts\activate.bat %ENVNAME%

rem set path to current BAT-file location (base dir)
cd %~dp0

rem start application
python OpenSourceDatabase_Dashboard.py