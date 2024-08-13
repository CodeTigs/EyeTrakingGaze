@echo off
chcp 65001

set grupo=laptop-jprle6fm\usuario

:: Verifica se o arquivo existe
if exist "C:\Program Files (x86)\GazePointer\GazePointer\GazePointer.exe" (
    :: Executa o comando icacls e redireciona a saída para um arquivo temporário para análise
    icacls "C:\Program Files (x86)\GazePointer\GazePointer\GazePointer.exe" /grant "%grupo%:(RX)" > temp_icacls_output.txt 2>&1
    if %errorlevel% neq 0 (
        echo Falha ao conceder permissão. Veja detalhes no arquivo temp_icacls_output.txt
        pause
        exit /b 1
    )
    :: Tenta abrir o programa
    start "" "C:\Program Files (x86)\GazePointer\GazePointer\GazePointer.exe"
    :: Verifica se houve erro na execução do comando
    if %errorlevel% equ 0 (
        echo Permissão concedida e programa iniciado com sucesso!
    ) else (
        echo Falha ao iniciar o programa. Verifique as permissões e o funcionamento do arquivo.
    )
) else (
    echo Arquivo não encontrado.
)

pause
