import os, shutil
import numpy as np
import deepdanbooru.project as ddproject
import concurrent.futures
from PIL import Image
from PIL.ExifTags import TAGS
from api.utils.string import getRootDir, getNowTime
from api.config.deepdanbooru import MODEL_PATH
import api.model.UserImage
import api.model.UserImageTag

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
                'platform': platform,
                'directory': directory,
                'path': f"{apiPath}/{directory}/{image}"
            })
            
        return response
    except Exception as e:
        return e
    
def __process_image(index, image, user_id, rootDir):
    try:
        result = dict({
            'user_id': user_id,
            'name': image['name'],
            'platform': image['platform'],
            'directory': image['directory'],
            'tags': dict(),
            'created_at': getNowTime('mysql'),
            'updated_at': getNowTime('mysql')
        })
        
        platform = image['platform']
        directory = image['directory']
        filename = image['name']
        
        path = f"{rootDir}/downloads/{platform}/images/{directory}/{filename}"
        
        targetImage = Image.open(path).convert('RGB')
        
        tags = __predict_tags(path, targetImage)
        
        shaped_tags = []
        for i, (name, confidence) in enumerate(tags.items()):
            args = dict()
            args['name_en'] = name
            args['confidence'] = round(confidence, 5)
            args['is_saved'] = True if confidence >= 0.5 else False
            shaped_tags.append(args)
                    
        result['tags'] = shaped_tags
        print(f"===== Tags generated for {filename}, index: {index} ===== ")
            
        return index, result
    except Exception as e:
        print(f"Error processing image at index {index}: {e}")
        return index, {'error': True, 'content': str(e)}
    
def generateTagsFromImage(images, user_id):
    rootDir = getRootDir()
    response = [None] * len(images)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(__process_image, i, image, user_id, rootDir): 
            i for i, image in enumerate(images)}
        for future in concurrent.futures.as_completed(futures):
            index, result = future.result()
            response[index] = result
    return response

def __predict_tags(path, image, threshold = 0.5):    
    model = ddproject.load_model_from_project(MODEL_PATH, compile_model=False)
    tags = ddproject.load_tags_from_project(MODEL_PATH)
    
    imageArray = __resize_and_transform_image(model, image)
    
    prediction = model.predict(imageArray)[0]
    result = {tags[i]: float(prediction[i]) for i in range(len(tags)) if prediction[i] > threshold}
    result = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
    return result

def __resize_and_transform_image(model, image: Image):
    # Resize and transform the image to the model input shape
    image_resized = image.resize((model.input_shape[2], model.input_shape[1]))
    image_array = np.array(image_resized)
    image_array = image_array / 255.0
    image_array = image_array[np.newaxis, ...]
    
    return image_array
    
def __getFileCount(directory):
    return len(os.listdir(directory)) if os.path.isdir(directory) else 0


def addTagsToImage(imagePath, tags):
    rootDir = getRootDir()
    path = f"{rootDir}/downloads/{path}"
    
    img = Image.open(path)
    exif = img.info.get('exif')
    
    for (index, tag) in enumerate(tags):
        if index >= 10:
            break
        exif_key = None
        for key, tag_name in TAGS.items():
            if tag_name == tag['tag_name']:
                exif_key = key
                break

def verifyImage(index, image, timestamp):
    rootDir = getRootDir()
    platform = image['platform']
    directory = image['directory']
    filename = image['name']
    
    try:
        path = f"{rootDir}/downloads/{platform}/images/{directory}/{filename}"
        # 画像をpathからimages/${Y-m-d_H-i-s}/${Y-m-d_H-i-s_${index}}.${extension}として保存
        extension = getFileExtension(path)
        newDir = f"{rootDir}/images/{timestamp}"
        newFilename = f"{timestamp}_{index}{extension}"
        newPath = f"{newDir}/{newFilename}"
        
        if not os.path.exists(newDir):
            os.mkdir(newDir)
        shutil.move(path, newPath)
        
        return newFilename
    except Exception as e:
        return {'error': True, 'content': f"Error saving image at index {index}: {e}"}
    
def saveImage(image, filename, user_id):
    created_at = image['created_at'] if 'created_at' in image else getNowTime('mysql')
    updated_at = image['updated_at'] if 'updated_at' in image else getNowTime('mysql')
    try:
        user_image_id = api.model.UserImage.create(
            user_id,
            filename,
            False,
            created_at,
            updated_at
        )
        
        if user_image_id == False:
            Exception('画像の保存に失敗しました。')
        
        tags = image['tags']
        
        for (index, tag) in enumerate(tags):
            if tag['is_saved'] == False:
                continue
            
            name_ja = None
            if 'name_ja' in tag:
                name_ja = tag['name_ja']
            
            api.model.UserImageTag.create(
                user_image_id,
                tag['name_en'],
                name_ja,
                tag['confidence']
            )
            
        return {'error': False, 'content': 'save success'}
    except Exception as e:
        return {'error': True, 'content': str(e)}
    
    
    
def getFileExtension(path):
    _, extension = os.path.splitext(path)
    return extension