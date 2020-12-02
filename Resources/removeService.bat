@echo off
setlocal
echo [96m Stopping Service: DLPExporter[0m
echo [96m-----------------------------[0m
echo.
..\Resources\nssm.exe stop DLPExporter
echo [96m Removing Service: DLPExporter[0m
echo [96m-----------------------------[0m
echo.
..\Resources\nssm.exe remove DLPExporter confirm
del ..\Resources\nssm.exe
rmdir \XMLFileCopy