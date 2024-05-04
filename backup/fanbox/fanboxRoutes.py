from flask import Blueprint, request, jsonify, make_response
import os, shutil
from api.imagedler.fanbox.getImage import setDriver, fanboxLogin, getImage
# from api.imagedler.fanbox.dlImage import dlImages
from api.utils.createPath import createPath
from api.utils.makeZip import makeZip 
from api.account.accountManager import AccountManager

fanboxRoutes = Blueprint('fanboxRoutes', __name__)

@fanboxRoutes.route('/fanbox/getImages', methods=['POST'])
async def getImages():
    data = request.get_json()
    searchQuery = data['content']
    pixivUserID = searchQuery['userID']
    url = searchQuery['url']
    
    print(pixivUserID)
    print(url)
    
    driver = setDriver()
    driver.maximize_window()
    accountManager = AccountManager()
    
    # await fanboxLogin(driver, url, pixivUserID, accountManager.getSingleData('pixiv_password'))
    imagePaths = await getImage(driver, url, pixivUserID, accountManager.getSingleData('pixiv_password'))
    # driver.quit()
    return imagePaths

@fanboxRoutes.route('/fanbox/downloadImages', methods=['POST'])
async def downloadImages():
    data = request.get_json()
    illusts = data['content']
    twitterPath = createPath('imagedler', 'twitter')
    imageDirPath = createPath(twitterPath, 'images')
    
    # 先に作成しているimagesフォルダを削除
    if os.path.exists(imageDirPath):
        shutil.rmtree(imageDirPath)
    
    # dlResult = await dlImages(imageDirPath, illusts)
    # if dlResult['error']:
    #     return jsonify({
    #         'error': True,
    #         'content': 'download failed'
    #     })
    # else:
    #     zipFilePath = makeZip(imageDirPath, twitterPath)
    #     return jsonify({
    #         'error': False,
    #         'content': 'download Success'
    #     })
        
@fanboxRoutes.route('/fanbox/getZip', methods=['GET'])
def getZip():
    zip_path = createPath('imagedler', 'twitter', 'images.zip')
    
    response = make_response()
    response.headers['Content-Type'] = 'application/octet-stream'
    response.headers['Content-Disposition'] = f'attachment; filename={os.path.basename(zip_path)}'
    response.data = open(zip_path, 'rb').read()

    return response