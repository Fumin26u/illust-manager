from flask import Flask, request, jsonify
from flask_cors import CORS
import os, requests, base64, cv2, shutil, json
import numpy as np
from io import BytesIO

from api.evaluate.eval import main as image_evaluate
from api.evaluate.detect_anime_face import load_checkpoint
from api.evaluate.createTrainData import createTrainData
from api.account.accountManager import AccountManager
from api.createPath import createPath
import api.save.saveImage as saveImage

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

@app.route('/', methods=['GET'])
def index():
    return 'This is an Index Page!'

@app.route('/api/getAccount', methods=['GET'])
def getAccount():
    accountManager = AccountManager(createPath('account', 'userdata.json'))
    username = accountManager.getUsername()
    return username

@app.route('/api/getModels', methods=['GET'])
def getModels():
    modelNames = sorted(os.listdir(createPath('evaluate', 'models')), reverse=True)
    return jsonify({'data': modelNames})

@app.route('/api/getImageDirs', methods=['GET'])
def getImageDirs():
    imageNames = sorted(os.listdir(createPath('evaluate', 'images')), reverse=True)
    return jsonify({'data': imageNames})
    
@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    # フロントから受け取ったjsonをbase64の配列に組み替え
    data = request.get_json()
    base64Images = data['imagePaths']
    modelPath = createPath('evaluate', 'models', data['model'])
    faceModelPath = createPath('evaluate', 'images', data['imageDir'])
    trainExtends = createTrainData(faceModelPath = faceModelPath)
    print(modelPath, faceModelPath)
    print('-----------')
    
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

@app.route('/api/save', methods=['POST'])
def save():
    # フロントから画像情報のjsonを取得
    data = request.get_json()
    imageInfo = data['imageInfo']
    minConfidence = float(data['minConfidence'])
    
    for image in imageInfo:
        confidence = float(image['confidence'].replace('%', ''))
        if (confidence >= minConfidence) or image['isImportant']:
            saveImage.saveImage(image['className'], image['imagePath'], image['rawPath'])
        else:
            saveImage.saveImage('others', image['imagePath'], image['rawPath'])
        
    return jsonify({'data': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
