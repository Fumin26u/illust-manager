from flask import Blueprint, request, jsonify

from api.evaluate.eval import main as image_evaluate
from api.face.detect_anime_face import load_checkpoint
from api.utils.createTrainData import createTrainData
from api.save.saveImage import saveImage
from api.utils.createPath import createPath
from api.utils.base64ToImage import base64ToImage, getImageExtension
from api.utils.createUuid import createUuid

import os, string, random
import concurrent.futures

evaluateRoutes = Blueprint('evaluateRoutes', __name__)

def generateRandomString(strLength: int) -> str:
    strArray = [random.choice(string.ascii_letters + string.digits) for i in range(strLength)]
    return ''.join(strArray)
    
@evaluateRoutes.route('/evaluate/getModels', methods=['GET'])
def getModels():
    modelNames = sorted(os.listdir(createPath('save', 'train_face_models')), reverse=True)
    return jsonify({'data': modelNames})

@evaluateRoutes.route('/evaluate/getImageDirs', methods=['GET'])
def getImageDirs():
    imageNames = sorted(os.listdir(createPath('save', 'face_images')), reverse=True)
    return jsonify({'data': imageNames})

@evaluateRoutes.route('/evaluate/evaluate', methods=['POST'])
def evaluate():
    # フロントから受け取ったjsonをbase64の配列に組み替え
    data = request.get_json()
    base64Images = data['imagePaths']
    modelPath = createPath('save', 'train_face_models', data['model'])
    faceModelPath = createPath('save', 'face_images', data['imageDir'])
    trainGenerator, validationGenerator = createTrainData(faceModelPath = faceModelPath)
    
    eachResults = []
    load_checkpoint()
    
    def evaluateSingleImage(args):
        i, base64Image = args['index'], args['imagePath']
        try:
            image = base64ToImage(base64Image)
            extension = '.' + getImageExtension(base64Image)
            result = image_evaluate(image, f'api/evaluate/{createUuid(8)}.jpg', trainGenerator, modelPath, extension=extension)
            return i, result
        except Exception as e:
            print(f"Error evaluating image: {str(e)}")
            return i, []
        
    # base64文字列を1つずつ画像に変換して評価(並列処理)
    with concurrent.futures.ThreadPoolExecutor() as executor: 
        futures = [executor.submit(evaluateSingleImage, base64Image) for base64Image in base64Images]
        
    results = [future.result() for future in concurrent.futures.as_completed(futures)]
    sorted_results = sorted(results, key=lambda x: x[0])  # インデックスでソート

    eachResults = [result for _, result in sorted_results]
    return jsonify({'data': eachResults})

@evaluateRoutes.route('/evaluate/save', methods=['POST'])
def save():
    # フロントから画像情報のjsonを取得
    data = request.get_json()
    imageInfo = data['imageInfo']
    minProbability = float(data['minProbability'])
    
    for image in imageInfo:
        probability = float(image['probability'].replace('%', ''))
        if (probability >= minProbability) or image['isImportant']:
            saveImage(image['className'], image['imagePath'], image['rawPath'])
        else:
            saveImage('others', image['imagePath'], image['rawPath'])
        
    return jsonify({'data': 'success'})