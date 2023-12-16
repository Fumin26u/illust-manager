from flask import Flask, request, jsonify
from flask_cors import CORS
import os, requests, base64, cv2, shutil
import numpy as np
from io import BytesIO

from api.evaluate.eval import main as image_evaluate
from api.evaluate.detect_anime_face import load_checkpoint
import api.save.saveImage as saveImage

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

@app.route('/', methods=['GET'])
def index():
    return 'This is an Index Page!'
    
@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    # フロントから受け取ったjsonをbase64の配列に組み替え
    data = request.get_json()
    base64Images = data['imagePaths']
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    modelPath = os.path.join(scriptDir, 'evaluate', 'models', 'model-2023-12-16-18-42-00.h5')
    
    eachResults = []
    load_checkpoint()
    # base64文字列を1つずつ画像に変換して評価
    for base64Image in base64Images:
        image_data = base64.b64decode(base64Image.split(',')[1])
        image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
        
        eachResults.append(image_evaluate(
            image, 
            'api/evaluate/eval.jpg', 
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
