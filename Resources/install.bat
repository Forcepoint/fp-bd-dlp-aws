START /WAIT powershell -command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest "https://nssm.cc/release/nssm-2.24.zip" -Method Get -OutFile .\Resources\nssm.zip"
START /WAIT powershell -command "Expand-Archive .\Resources\nssm.zip .\Resources"
move .\Resources\nssm-2.24\win64\nssm.exe .\Resources
del .\Resources\nssm.zip
rmdir .\Resources\nssm-2.24 /s/q
@echo off
setlocal
echo [Creating required directories]
echo [-----------------------------]
echo.
mkdir \XMLFileCopy
echo.
@echo off
echo [Log into Database]
echo [-----------------]
echo.
set /P option="Are you using a trusted Database connection in your config? (y/n): "
if %option%==y goto continue
if %option%==n goto passwordLogin

:passwordLogin
C:\fp-dlp-exporter-aws-azure-v1\DLPExporter.exe --login=login
goto continue

:continue
echo [Creating Service: DLPExporter]
echo [-----------------------------]
C:\fp-dlp-exporter-aws-azure-v1\Service.exe