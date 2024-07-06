from flask import Blueprint, request, jsonify, make_response
import os, shutil
from api.imagedler.twitter.getTweetInfo import setDriver, twitterLogin, getTweet
from api.imagedler.twitter.dlImage import dlImages
from api.utils.createPath import createPath
from api.utils.makeZip import makeZip 
from api.account.accountManager import AccountManager

twitterController = Blueprint('twitterController', __name__)
basePath = '/api/twitter'

@twitterController.route(f"{basePath}/getImages", methods=['POST'])
async def getImages():
    data = request.get_json()
    searchQuery = data['content']
    driver = setDriver()
    accountManager = AccountManager()
    
    twitterLogin(driver, searchQuery['twitterID'], accountManager.getSingleData('twitter_password'))
    tweetInfo = getTweet(driver, searchQuery)
    driver.quit()
    return tweetInfo

@twitterController.route('/twitter/downloadImages', methods=['POST'])
async def downloadImages():
    data = request.get_json()
    illusts = data['content']
    twitterPath = createPath('imagedler', 'twitter')
    imageDirPath = createPath(twitterPath, 'images')
    
    # 先に作成しているimagesフォルダを削除
    if os.path.exists(imageDirPath):
        shutil.rmtree(imageDirPath)
    
    dlResult = await dlImages(imageDirPath, illusts)
    if dlResult['error']:
        return jsonify({
            'error': True,
            'content': 'download failed'
        })
    else:
        zipFilePath = makeZip(imageDirPath, twitterPath)
        return jsonify({
            'error': False,
            'content': 'download Success'
        })
        
@twitterController.route('/twitter/getZip', methods=['GET'])
def getZip():
    zip_path = createPath('imagedler', 'twitter', 'images.zip')
    
    response = make_response()
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment; filename={os.path.basename(zip_path)}'
    response.data = open(zip_path, 'rb').read()

    return response