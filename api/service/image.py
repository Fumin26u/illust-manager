import os

from api.utils.string import getRootDir

def getDirectories(platform = 'local'):
    rootDir = getRootDir()
    try:
        path = f"{rootDir}/downloads/{platform}/images"
        directories = sorted(os.listdir(path))
        
        response = []
        for directory in directories:
            targetPath = f"{path}/{directory}"
            response.append({
                'name': directory,
                'count': __getFileCount(targetPath)
            })
            
        return response
    except Exception as e:
        return e

def loadImages(directory, platform = 'local'):
    rootDir = getRootDir()
    try:
        path = f"{rootDir}/downloads/{platform}/images/{directory}"
        apiPath = f"api/image/{platform}"
        images = sorted(os.listdir(path))
        
        response = []
        for image in images:
            response.append({
                'name': image,
                'path': f"{apiPath}/{directory}/{image}"
            })
            
        return response
    except Exception as e:
        return e
    
def __getFileCount(directory):
    return len(os.listdir(directory)) if os.path.isdir(directory) else 0