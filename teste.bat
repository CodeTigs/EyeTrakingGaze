::icacls "C:\Program Files (x86)\GazePointer\GazePointer\GazePointer.exe"
::icacls "C:\Program Files (x86)\GazePointer\GazePointer\GazePointer.exe" /grant "BUILTIN\Administradores:(OI)(CI)(M)"
::BUILTIN\Administradores

@echo off
setlocal

REM Defina o caminho completo do arquivo que deseja verificar
set "arquivo=C:\Program Files (x86)\GazePointer\GazePointer\GazePointer.exe"

REM Use o comando icacls para obter as permissões do arquivo
icacls "%arquivo%" > permissoes.txt

REM Abra o arquivo de texto com as permissões
notepad permissoes.txt