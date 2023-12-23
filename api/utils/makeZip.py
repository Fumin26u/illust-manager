import os, subprocess
def makeZip(imageDirPath, zipSavePath, zipFileName = 'images.zip'):
    zipFilePath = os.path.join(zipSavePath, zipFileName)
    # 先に作成しているzipファイルを削除
    if os.path.exists(zipFilePath):
        os.remove(zipFilePath)
    
    # zipコマンドを実行してディレクトリを圧縮
    try:
        subprocess.run(['zip', '-r', zipFilePath, '.'], cwd=imageDirPath, check=True)
        return zipFilePath
    except subprocess.CalledProcessError as e:
        print(f"Error during zip creation: {e}")
        return None
    
def deleteZip(imageDirPath, zipFileName):
    zipFilePath = os.path.join(imageDirPath, zipFileName)
    os.remove(zipFilePath)