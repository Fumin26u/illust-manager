from flask import Blueprint, request, jsonify

import os, base64, cv2, string, random, uuid
import numpy as np
import concurrent.futures

from api.utils.createPath import createPath
from api.utils.base64ToImage import base64ToImage, getImageExtension
from api.utils.getNowTime import getNowTime
from api.utils.createUuid import createUuid
from api.face.getFace import cropImageToFace

cropRoutes = Blueprint('cropRoutes', __name__)

@cropRoutes.route('/crop/cropImage', methods=['POST'])
def cropImage():
    data = request.get_json()
    base64Images = data.get('imagePaths', [])
    
    try:
        def cropSingleImage(base64Image):
            childDir, image = base64Image['childDir'], base64ToImage(base64Image['imageInfo'])
            extension = getImageExtension(base64Image['imageInfo'])
            savePath = createPath('save', 'face_images', getNowTime(), childDir)
            
            if not os.path.exists(savePath):
                os.mkdir(savePath)
            cropImageToFace(image, savePath, f'{createUuid(8)}{extension}')
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(cropSingleImage, base64Images)
        
        return jsonify({'error': False, 'content': 'done'})
    except Exception as e:
        print(f"Error cropping image: {str(e)}")
        return jsonify({'error': True, 'content': {str(e)}})