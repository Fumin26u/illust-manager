from flask import Blueprint, request, jsonify, make_response
from api.imagedler.pixiv.getImage import main as getPixivImage
from api.imagedler.pixiv.dlImage import main as downloadPixivImage
from api.makeZip import makeZip
from api.createPath import createPath

import os, shutil

pixivRoutes = Blueprint('pixivRoutes', __name__)


@pixivRoutes.route('/api/getPixivImages', methods=['POST'])
async def getPixivImages():
    data = request.get_json()
    searchQuery = data['content']
    return await getPixivImage(searchQuery)

@pixivRoutes.route('/api/downloadPixivImages', methods=['GET', 'POST'])
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
    
@pixivRoutes.route('/api/getZip', methods=['GET'])
def getZip():
    zip_path = createPath('imagedler', 'pixiv', 'images.zip')
    
    response = make_response()
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment; filename={os.path.basename(zip_path)}'
    response.data = open(zip_path, 'rb').read()

    return response