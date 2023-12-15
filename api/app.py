from flask import Flask, request, jsonify
from flask_cors import CORS
import os, requests, base64, cv2
import numpy as np
from io import BytesIO

from api.evaluate.eval import main as image_evaluate
from api.evaluate.detect_anime_face import load_checkpoint

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
    modelPath = os.path.join(scriptDir, 'evaluate', 'models', 'model-2023-12-03-23-01-33.h5')
    
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

if __name__ == '__main__':
    app.run(debug=True)
