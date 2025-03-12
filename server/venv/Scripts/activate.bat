@echo off

rem This file is UTF-8 encoded, so we need to update the current code page while executing it
for /f "tokens=2 delims=:." %%a in ('"%SystemRoot%\System32\chcp.com"') do (
    set _OLD_CODEPAGE=%%a
)
if defined _OLD_CODEPAGE (
    "%SystemRoot%\System32\chcp.com" 65001 > nul
)

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
set "VIRTUAL_ENV=D:\Estudos\Projetos\Web\EduManager\server\venv"
=======
set VIRTUAL_ENV=C:\Users\uliss\OneDrive\Área de Trabalho\EduManager\EduManager\server\venv
>>>>>>> origin/usuario-cc
=======
set VIRTUAL_ENV=C:\Users\levi_\Desktop\ES2\EduManager\server\venv
>>>>>>> calendario-cc
=======
set "VIRTUAL_ENV=C:\Users\miste\EduManager\server\venv"
>>>>>>> disciplina-cc

if not defined PROMPT set PROMPT=$P$G

if defined _OLD_VIRTUAL_PROMPT set PROMPT=%_OLD_VIRTUAL_PROMPT%
if defined _OLD_VIRTUAL_PYTHONHOME set PYTHONHOME=%_OLD_VIRTUAL_PYTHONHOME%

<<<<<<< HEAD
<<<<<<< HEAD
set "_OLD_VIRTUAL_PROMPT=%PROMPT%"
set "PROMPT=(venv) %PROMPT%"
=======
set _OLD_VIRTUAL_PROMPT=%PROMPT%
set PROMPT=(venv) %PROMPT%
>>>>>>> origin/usuario-cc
=======
set _OLD_VIRTUAL_PROMPT=%PROMPT%
set PROMPT=(venv) %PROMPT%
>>>>>>> calendario-cc

if defined PYTHONHOME set _OLD_VIRTUAL_PYTHONHOME=%PYTHONHOME%
set PYTHONHOME=

if defined _OLD_VIRTUAL_PATH set PATH=%_OLD_VIRTUAL_PATH%
if not defined _OLD_VIRTUAL_PATH set _OLD_VIRTUAL_PATH=%PATH%

<<<<<<< HEAD
<<<<<<< HEAD
set "PATH=%VIRTUAL_ENV%\Scripts;%PATH%"
set "VIRTUAL_ENV_PROMPT=venv"
=======
set PATH=%VIRTUAL_ENV%\Scripts;%PATH%
set VIRTUAL_ENV_PROMPT=(venv) 
>>>>>>> origin/usuario-cc
=======
set PATH=%VIRTUAL_ENV%\Scripts;%PATH%
set VIRTUAL_ENV_PROMPT=(venv) 
>>>>>>> calendario-cc

:END
if defined _OLD_CODEPAGE (
    "%SystemRoot%\System32\chcp.com" %_OLD_CODEPAGE% > nul
    set _OLD_CODEPAGE=
)
