START /WAIT powershell -command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest "https://nssm.cc/release/nssm-2.24.zip" -Method Get -OutFile .\Resources\nssm.zip"
START /WAIT powershell -command "Expand-Archive .\Resources\nssm.zip .\Resources"
move .\Resources\nssm-2.24\win64\nssm.exe .\Resources
del .\Resources\nssm.zip
rmdir .\Resources\nssm-2.24 /s/q
@echo off
setlocal
echo [96m Creating required directories[0m
echo [96m-----------------------------[0m
echo.
mkdir \XMLFileCopy
echo.
echo [96m Creating Service: DLPExporter[0m
echo [96m-----------------------------[0m
set /P user="Please enter your username: "
set /P password="Please enter your administrator password: "
Resources\nssm.exe install DLPExporter C:\fp-dlp-exporter-aws-azure-v1\DLPExporter.exe
Resources\nssm.exe set DLPExporter AppDirectory C:\fp-dlp-exporter-aws-azure-v1
Resources\nssm.exe set DLPExporter AppStdout C:\fp-dlp-exporter-aws-azure-v1\logs\ForcepointDLPEvents.log
Resources\nssm.exe set DLPExporter AppStderr C:\fp-dlp-exporter-aws-azure-v1\logs\ForcepointDLPEvents.log
Resources\nssm.exe set DLPExporter ObjectName %user% %password%
Resources\nssm.exe start DLPExporter
pause