from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
import os, requests, base64, cv2, shutil, json
import numpy as np
from io import BytesIO

from api.evaluate.eval import main as image_evaluate
from api.evaluate.detect_anime_face import load_checkpoint
from api.evaluate.createTrainData import createTrainData
from api.account.accountManager import AccountManager
from api.createPath import createPath
from api.makeZip import makeZip
from api.imagedler.pixiv.getImage import main as getPixivImage
from api.imagedler.pixiv.dlImage import main as downloadPixivImage
import api.save.saveImage as saveImage

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
accountManager = AccountManager(createPath('account', 'userdata.json'))

@app.route('/', methods=['GET'])
def index():
    return 'This is an Index Page!'

@app.route('/api/getAccount', methods=['GET'])
def getAccount():
    username = accountManager.getSingleData('user_name')
    return username

@app.route('/api/getPixivInfo', methods=['GET'])
def getPixivInfo():
    pixivInfo = accountManager.getPixivInfo()
    return pixivInfo

@app.route('/api/getPixivImages', methods=['POST'])
async def getPixivImages():
    data = request.get_json()
    searchQuery = data['content']
    return await getPixivImage(searchQuery)

@app.route('/api/downloadPixivImages', methods=['GET', 'POST'])
async def downloadPixivImages():
    data = request.get_json()
    illusts = data['content']
    pixivPath = createPath('imagedler', 'pixiv')
    imageDirPath = createPath(pixivPath, 'images')
    
    # 先に作成しているimagesフォルダを削除
    if os.path.exists(imageDirPath):
        shutil.rmtree(imageDirPath)
    
    dlResult = await downloadPixivImage(imageDirPath, illusts)
    if dlResult['error']:
        return jsonify({
            'error': True,
            'content': 'download failed'
        })
    else:
        zipFilePath = makeZip(imageDirPath, pixivPath)
        return jsonify({
            'error': False,
            'content': 'download Success'
        })
    
@app.route('/api/getZip', methods=['GET'])
def getZip():
    zip_path = createPath('imagedler', 'pixiv', 'images.zip')
    
    response = make_response()
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment; filename={os.path.basename(zip_path)}'
    response.data = open(zip_path, 'rb').read()

    return response

@app.route('/api/updatePixivInfo', methods=['POST'])
def updatePixivInfo():
    dlCount = accountManager.getSingleData('dl_count')
    imagesCount = accountManager.getSingleData('images_count')
    pixivAccounts = accountManager.getSingleData('pixiv')
    
    data = request.get_json()
    imagesCount += int(data['imageCount'])
    dlCount += 1
    
    isIdExists = False
    for (i, pixivAccount) in enumerate(pixivAccounts):
        if pixivAccount['id'] == str(data['pixUserID']):
            pixivAccounts[i]['post'] = str(data['latestID'])
            isIdExists = True
            
    if not isIdExists:
        pixivAccounts.append({
            'id': str(data['pixUserID']),
            'post': str(data['latestID'])
        })
        
    accountManager.update('dl_count', dlCount)
    accountManager.update('images_count', imagesCount)
    # accountManager.update('pixiv', pixivAccounts)
    
    return 'success'
    
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
