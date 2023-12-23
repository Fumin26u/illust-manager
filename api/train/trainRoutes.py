from flask import Blueprint, request, jsonify

import os, base64, cv2, string, random, uuid
import numpy as np
import concurrent.futures

from api.utils.createPath import createPath
from api.utils.getNowTime import getNowTime
from api.utils.createUuid import createUuid
from api.utils.createTrainData import createTrainData
from api.train.train import main as createTrainModel

trainRoutes = Blueprint('trainRoutes', __name__)

@trainRoutes.route('/train/train', methods=['POST'])
def train():
    data = request.get_json()
    path = data.get('path', '')
    
    try:
        referencePath = createPath('save', 'face_images', path)
        trainExtends = createTrainData(referencePath)
        
        savePath = createPath('save', 'train_face_models', f'model-{getNowTime()}.h5')
        createTrainModel(trainExtends, referencePath, savePath)
        
        return jsonify({'error': False, 'content': f'success, save path: {savePath}'})
    except Exception as e:
        print(f"Error training model: {str(e)}")
        return jsonify({'error': True, 'content': {str(e)}})