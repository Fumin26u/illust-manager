import os, subprocess
from time import sleep
def createZip(imageDirPath, zipFilePath):    
    try:
        subprocess.run(['zip', '-r', zipFilePath, '.'], cwd=imageDirPath, check=True)
        return zipFilePath
    except subprocess.CalledProcessError as e:
        return {'error': True, 'content': e}
    
def deleteZipFiles(zipSavePath):
    for file in os.listdir(zipSavePath):
        if file.endswith('.zip'):
            os.remove(os.path.join(zipSavePath, file))
            
def getZipFileName(zipSavePath):
    sleep(1)
    for file in os.listdir(zipSavePath):
        if file.endswith('.zip'):
            return file
    return None