import os
import numpy as np
import deepdanbooru.project as ddproject
import deepdanbooru.data as dddata
from tensorflow import keras
from keras.models import load_model
from PIL import Image
from api.utils.string import getRootDir
from api.config.deepdanbooru import MODEL_PATH

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
    
def generateTagsFromImage(images):
    rootDir = getRootDir()
    response = []
    try:
        for image in images:
            result = dict({
                'name': image['name'],
                'platform': image['platform'],
                'directory': image['directory'],
                'tags': dict()
            })
            
            platform = image['platform']
            directory = image['directory']
            filename = image['name']
            
            path = f"{rootDir}/downloads/{platform}/images/{directory}/{filename}"
            
            targetImage = Image.open(path).convert('RGB')
            
            tags = __predict_tags(path, targetImage)
            result['tags'] = tags
            response.append(result)
            
        return response
    except Exception as e:
        return {'error': True, 'content': e}

def __predict_tags(path, image, threshold = 0.5):
    # load tag/model
    
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