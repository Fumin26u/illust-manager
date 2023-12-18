from flask import Blueprint, request, jsonify
from api.evaluate.eval import main as image_evaluate
from api.evaluate.detect_anime_face import load_checkpoint
from api.evaluate.createTrainData import createTrainData
from api.save.saveImage import saveImage
from api.createPath import createPath

import os, base64, cv2
import numpy as np

evaluateRoutes = Blueprint('evaluateRoutes', __name__)
    
@evaluateRoutes.route('/api/getModels', methods=['GET'])
def getModels():
    modelNames = sorted(os.listdir(createPath('evaluate', 'models')), reverse=True)
    return jsonify({'data': modelNames})

@evaluateRoutes.route('/api/getImageDirs', methods=['GET'])
def getImageDirs():
    imageNames = sorted(os.listdir(createPath('evaluate', 'images')), reverse=True)
    return jsonify({'data': imageNames})

@evaluateRoutes.route('/api/evaluate', methods=['POST'])
def evaluate():
    # フロントから受け取ったjsonをbase64の配列に組み替え
    data = request.get_json()
    base64Images = data['imagePaths']
    modelPath = createPath('evaluate', 'models', data['model'])
    faceModelPath = createPath('evaluate', 'images', data['imageDir'])
    trainExtends = createTrainData(faceModelPath = faceModelPath)
    
    eachResults = []
    load_checkpoint()
    # base64文字列を1つずつ画像に変換して評価
    for base64Image in base64Images:
        image_data = base64.b64decode(base64Image.split(',')[1])
        image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
        
        eachResults.append(image_evaluate(
            image, 
            'api/evaluate/eval.jpg', 
            trainExtends,
            modelPath
        ))
    return jsonify({'data': eachResults})

@evaluateRoutes.route('/api/save', methods=['POST'])
def save():
    # フロントから画像情報のjsonを取得
    data = request.get_json()
    imageInfo = data['imageInfo']
    minConfidence = float(data['minConfidence'])
    
    for image in imageInfo:
        confidence = float(image['confidence'].replace('%', ''))
        if (confidence >= minConfidence) or image['isImportant']:
            saveImage(image['className'], image['imagePath'], image['rawPath'])
        else:
            saveImage('others', image['imagePath'], image['rawPath'])
        
    return jsonify({'data': 'success'})