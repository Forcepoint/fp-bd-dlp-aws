import os

if __name__ == "__main__":
    username = input('Please enter your domain\\administrator username e.g.(.\\Administrator): ')
    password = input('Please enter your administrator password: ')
    os.system('Resources\\nssm.exe install DLPExporter C:\\fp-dlp-exporter-aws-azure-v1\\DLPExporter.exe')
    os.system('Resources\\nssm.exe set DLPExporter AppDirectory C:\\fp-dlp-exporter-aws-azure-v1')
    os.system(
        'Resources\\nssm.exe set DLPExporter AppStdout C:\\fp-dlp-exporter-aws-azure-v1\\logs\\ForcepointDLPEvents.log')
    os.system(
        'Resources\\nssm.exe set DLPExporter AppStderr C:\\fp-dlp-exporter-aws-azure-v1\\logs\\ForcepointDLPEvents.log')
    os.system(f'Resources\\nssm.exe set DLPExporter ObjectName \"{username}\" \"{password}\"')
    os.system('Resources\\nssm.exe start DLPExporter')
    os.system('pause')
