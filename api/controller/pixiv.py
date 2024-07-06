from flask import Blueprint, request, jsonify, make_response
from api.imagedler.pixiv.getImage import main as getImage
from api.imagedler.pixiv.dlImage import main as downloadImage
from api.utils.makeZip import makeZip, deleteZipFiles, getZipFileName
from api.utils.createPath import createPath

import os, shutil
from urllib.parse import quote

pixivController = Blueprint('pixivController', __name__)

@pixivController.route('/pixiv/getImages', methods=['POST'])
async def getImages():
    data = request.get_json()
    searchQuery = data['content']
    return await getImage(searchQuery)
    # return searchQuery

@pixivController.route('/pixiv/downloadImages', methods=['POST'])
async def downloadImages():
    data = request.get_json()
    illusts = data['content']
    pixivPath = createPath('imagedler', 'pixiv')
    imageDirPath = createPath(pixivPath, 'images')
    zipFileName = data['dlName'] + '.zip' if data['dlName'] != '' else 'images.zip'
    
    # 先に作成しているimagesフォルダを削除
    if os.path.exists(imageDirPath):
        shutil.rmtree(imageDirPath)
    
    dlResult = await downloadImage(imageDirPath, illusts)
    if dlResult['error']:
        return jsonify({
            'error': True,
            'content': 'download failed'
        })
    else:
        makeZip(imageDirPath, pixivPath, zipFileName)
        return jsonify({
            'error': False,
            'content': 'download Success'
        })
    
@pixivController.route('/pixiv/getZip', methods=['GET'])
def getZip():
    pixivPath = createPath('imagedler', 'pixiv')
    zipFileName = getZipFileName(pixivPath)
    zip_path = f'{pixivPath}\\{zipFileName}'
    print(zip_path)
    
    response = make_response()
    response.headers['Content-Type'] = 'application/octet-stream'
    encodedFilename = quote(zipFileName.encode('utf-8'))
    
    response.headers['Content-Disposition'] = f'attachment; filename={encodedFilename}'
    response.data = open(zip_path, 'rb').read()

    return response