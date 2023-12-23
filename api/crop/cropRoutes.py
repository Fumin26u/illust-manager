from flask import Blueprint, request, jsonify

import os, base64, cv2, string, random, uuid
import numpy as np
import concurrent.futures

from api.utils.createPath import createPath
from api.utils.base64ToImage import base64ToImage, getImageExtension
from api.utils.getNowTime import getNowTime
from api.utils.createUuid import createUuid
from api.face.getFace import cropImageToFace
from api.face.detect_anime_face import load_checkpoint

cropRoutes = Blueprint('cropRoutes', __name__)

@cropRoutes.route('/crop/cropImage', methods=['POST'])
def cropImage():
    data = request.get_json()
    base64Images = data.get('content', [])
    currentTime = data.get('currentTime', getNowTime())
    usingOldModel = data.get('usingOldModel', False)
    savePath_parent = createPath('save', 'face_images', f'faces_{currentTime}')
    if not os.path.exists(savePath_parent):
        os.mkdir(savePath_parent)
        
    load_checkpoint()
    
    try:
        def cropSingleImage(base64Image):
            childDir, image = base64Image['childDir'], base64ToImage(base64Image['imageInfo'])
            extension = '.' + getImageExtension(base64Image['imageInfo'])
            savePath = createPath(savePath_parent, childDir)
            
            if not os.path.exists(savePath):
                os.mkdir(savePath)
            
            faces = cropImageToFace(image, extension=extension, usingOldModel=usingOldModel)
            saveFileName = f'{savePath}\\{createUuid(8)}{extension}'
            with open(saveFileName, 'wb') as f:
                f.write(faces[0])
            # for face in faces:
            #     saveFileName = f'{savePath}\\{createUuid(8)}{extension}'
            #     with open(saveFileName, 'wb') as f:
            #         f.write(face)
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(cropSingleImage, base64Images)
        
        return jsonify({'error': False, 'content': f'success, save path: {savePath_parent}'})
    except Exception as e:
        print(f"Error cropping image: {str(e)}")
        return jsonify({'error': True, 'content': {str(e)}})