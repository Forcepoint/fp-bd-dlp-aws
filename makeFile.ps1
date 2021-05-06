Write-Output [96m Installing PIP[0m
Write-Output [96m----------------[0m
Write-Output -
Write-Output -
python Resources\get-pip.py

Write-Output [96m Installing required packages[0m
Write-Output [96m-----------------------------[0m
Write-Output -
Write-Output -
python -m pip install -r requirements.txt
pip install git+git://github.com/pyinstaller/pyinstaller.git@9dd34bdfbaeaa4e0459bd3051d1caf0c7d75073f

Write-Output [96m Creating python exe[0m
Write-Output [96m-----------------------------[0m
Write-Output -
Write-Output -
pyinstaller --onefile DLPExporter.py

Write-Output [96m Choose modules to be installed[0m
Write-Output [96m--------------------------------[0m
Write-Output .
$azure=Read-Host "Do you want azure configured on y/n?"
$aws=Read-Host "Do you want aws configured on y/n?"


Write-Output [96m Creating required directories[0m
Write-Output [96m-----------------------------[0m
Write-Output -
Write-Output -
mkdir .\fp-dlp-exporter-aws-azure-v1
mkdir .\fp-dlp-exporter-aws-azure-v1\CloudFormationTemplate
mkdir .\fp-dlp-exporter-aws-azure-v1\Remediation_script
mkdir .\fp-dlp-exporter-aws-azure-v1\Resources
xcopy .\Resources .\fp-dlp-exporter-aws-azure-v1\Resources /s /e
move-item .\dist\DLPExporter.exe .\fp-dlp-exporter-aws-azure-v1
move-item .\fp-dlp-exporter-aws-azure-v1\Resources\install.bat .\fp-dlp-exporter-aws-azure-v1
mkdir .\fp-dlp-exporter-aws-azure-v1\ServiceScripts
move-item .\fp-dlp-exporter-aws-azure-v1\Resources\restart.bat .\fp-dlp-exporter-aws-azure-v1\ServiceScripts
move-item .\fp-dlp-exporter-aws-azure-v1\Resources\stopService.bat .\fp-dlp-exporter-aws-azure-v1\ServiceScripts
move-item .\fp-dlp-exporter-aws-azure-v1\Resources\removeService.bat .\fp-dlp-exporter-aws-azure-v1\ServiceScripts
move-item .\fp-dlp-exporter-aws-azure-v1\Resources\changePassword.bat .\fp-dlp-exporter-aws-azure-v1\ServiceScripts
xcopy .\CloudFormationTemplate .\fp-dlp-exporter-aws-azure-v1\CloudFormationTemplate /s /e
xcopy .\Remediation_script .\fp-dlp-exporter-aws-azure-v1\Remediation_script /s /e
xcopy .\config.json .\fp-dlp-exporter-aws-azure-v1
Remove-Item –path .\fp-dlp-exporter-aws-azure-v1\Resources\get-pip.py –recurse

$awsInstall=$false

if ($aws -eq 'y' -or $aws -eq "Y") {
    $awsInstall=$true
}
if ($awsInstall -eq $false) {
    Remove-Item –path .\fp-dlp-exporter-aws-azure-v1\Resources\AWSDate.json –recurse
    Remove-Item –path .\fp-dlp-exporter-aws-azure-v1\Resources\Insights.json –recurse
    Remove-Item –path .\fp-dlp-exporter-aws-azure-v1\Resources\InsightARN.json –recurse
    Remove-Item –path .\fp-dlp-exporter-aws-azure-v1\CloudFormationTemplate –recurse
    Remove-Item –path .\fp-dlp-exporter-aws-azure-v1\Remediation_script –recurse
    $LineNumber = 2
    $Contents = Get-Content .\fp-dlp-exporter-aws-azure-v1\config.json
    $Contents -replace $Contents[$LineNumber -1],"" | Set-Content .\fp-dlp-exporter-aws-azure-v1\config.json
    $LineNumber = 3
    $Contents = Get-Content .\fp-dlp-exporter-aws-azure-v1\config.json
    $Contents -replace $Contents[$LineNumber -1],"" | Set-Content .\fp-dlp-exporter-aws-azure-v1\config.json
    $LineNumber = 4
    $Contents = Get-Content .\fp-dlp-exporter-aws-azure-v1\config.json
    $Contents -replace $Contents[$LineNumber -1],"" | Set-Content .\fp-dlp-exporter-aws-azure-v1\config.json
    $LineNumber = 5
    $Contents = Get-Content .\fp-dlp-exporter-aws-azure-v1\config.json
    $Contents -replace $Contents[$LineNumber -1],"" | Set-Content .\fp-dlp-exporter-aws-azure-v1\config.json
    $LineNumber = 6
    $Contents = Get-Content .\fp-dlp-exporter-aws-azure-v1\config.json
    $Contents -replace $Contents[$LineNumber -1],"" | Set-Content .\fp-dlp-exporter-aws-azure-v1\config.json

}

$azureInstall=$false

if ($azure -eq 'y' -or $azure -eq "Y") {
    $azureInstall=$true
}
if ($azureInstall -eq $false) {
    Remove-Item –path .\fp-dlp-exporter-aws-azure-v1\Resources\azureDate.json –recurse
    $LineNumber = 18
    $Contents = Get-Content .\fp-dlp-exporter-aws-azure-v1\config.json
    $Contents -replace $Contents[$LineNumber -1],"" | Set-Content .\fp-dlp-exporter-aws-azure-v1\config.json
    $LineNumber = 19
    $Contents = Get-Content .\fp-dlp-exporter-aws-azure-v1\config.json
    $Contents -replace $Contents[$LineNumber -1],"" | Set-Content .\fp-dlp-exporter-aws-azure-v1\config.json

}


Write-Output [96m Creating fp-dlp-exporter-aws-azure-v1-8-3.zip[0m
Write-Output [96m-----------------------------[0m
Write-Output -
Write-Output -


Compress-Archive .\fp-dlp-exporter-aws-azure-v1 .\fp-dlp-exporter-aws-azure-v1-8-3.zip
Write-Output [96m Clean up[0m
Write-Output [96m-----------------------------[0m
Write-Output -
Write-Output -
Remove-Item –path .\__pycache__ –recurse
Remove-Item –path .\fp-dlp-exporter-aws-azure-v1 –recurse
Remove-Item –path .\build –recurse
Remove-Item –path .\dist –recurse
Remove-Item –path .\DLPExporter.spec –recurse