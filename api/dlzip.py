import os
import zipfile
def makeZip(imageDirPath, zipFileName):
    zipFilePath = os.path.join(imageDirPath, zipFileName)

    # ディレクトリ内のファイルをzip圧縮
    try:
        with zipfile.ZipFile(zipFilePath, 'w') as zip_file:
            for root, _, files in os.walk(imageDirPath):
                for file in files:
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, os.path.relpath(file_path, imageDirPath))

        return zipFilePath
    except Exception as e:
        print(f"Error during zip creation: {e}")
        return None