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
set /P option="Is this your first login? (y/n): "
if %option%==y goto passwordLogin
if %option%==n goto keyLogin

:passwordLogin
set /P dbuser="Please enter your Database username: "
set /P dbpassword="Please enter your Database password: "
set /A key="None"
goto continue

:keyLogin
set /P dbuser="Please enter your Database username: "
set /P key="Please enter your key: "
goto continue

:continue
echo [Creating Service: DLPExporter]
echo [-----------------------------]
set /P user="Please enter your domain\administrator username e.g.(.\Administrator): "
set /P password="Please enter your administrator password: "
Resources\nssm.exe install DLPExporter C:\fp-dlp-exporter-aws-azure-v1\DLPExporter.exe --password=%dbpassword% --username=%dbuser% --key=%key%
Resources\nssm.exe set DLPExporter AppDirectory C:\fp-dlp-exporter-aws-azure-v1
Resources\nssm.exe set DLPExporter AppStdout C:\fp-dlp-exporter-aws-azure-v1\logs\ForcepointDLPEvents.log
Resources\nssm.exe set DLPExporter AppStderr C:\fp-dlp-exporter-aws-azure-v1\logs\ForcepointDLPEvents.log
Resources\nssm.exe set DLPExporter ObjectName %user% %password%
Resources\nssm.exe start DLPExporter
pause