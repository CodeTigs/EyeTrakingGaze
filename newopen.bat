@echo off
setlocal

chcp 65001

REM Defina o caminho completo do arquivo .exe que deseja executar
set "executavel=C:\Program Files (x86)\GazePointer\GazePointer\GazePointer.exe"

REM Defina o nome de usuário que você deseja usar
set "usuario=BUILTIN\Usuários"

REM Usar o comando runas para executar o .exe com outro usuário
runas /user:%usuario% "%executavel%"

::<|°_°|>