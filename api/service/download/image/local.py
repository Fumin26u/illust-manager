import os, cv2

from api.utils.string import generateRandomString
from api.utils.base64ToImage import base64ToImage, getImageExtension

async def importImage(savePath, images):
    try:
        if not os.path.exists(savePath):
            os.mkdir(savePath)
            
        imported_paths = []
        file_names = []
            
        for (index, image) in enumerate(images):
            extension = getImageExtension(image['base64'])
            image = base64ToImage(image['base64'])
             
            fileName = image['name'] if 'name' in image else f"{generateRandomString(12)}.{extension}"
            cv2.imwrite(f"{savePath}/{fileName}", image)
            
            imported_paths.append(f"{savePath}/{fileName}")
            file_names.append(fileName)
            
        return {'error': False, 'imported_paths': imported_paths, 'file_names': file_names}
    except Exception as e:
        return {'error': True, 'content': e}