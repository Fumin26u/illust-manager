from flask import Blueprint, request, jsonify
from api.account.accountManager import AccountManager
from api.createPath import createPath

accountRoutes = Blueprint('accountRoutes', __name__)
accountManager = AccountManager(createPath('account', 'userdata.json'))

@accountRoutes.route('/api/getAccount', methods=['GET'])
def getAccount():
    username = accountManager.getSingleData('user_name')
    return username

@accountRoutes.route('/api/getPixivInfo', methods=['GET'])
def getPixivInfo():
    pixivInfo = accountManager.getPixivInfo()
    return pixivInfo

@accountRoutes.route('/api/updatePixivInfo', methods=['POST'])
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