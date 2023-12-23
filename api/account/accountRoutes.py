from flask import Blueprint, request, jsonify
from api.account.accountManager import AccountManager
from api.utils.createPath import createPath

accountRoutes = Blueprint('accountRoutes', __name__)
accountManager = AccountManager(createPath('account', 'userdata.json'))
print(createPath('account', 'userdata.json'))

@accountRoutes.route('/api/getAccount', methods=['GET'])
def getAccount():
    username = accountManager.getSingleData('user_name')
    return username

@accountRoutes.route('/api/getPixivInfo', methods=['GET'])
def getPixivInfo():
    pixivInfo = accountManager.getSingleData('pixiv')
    return pixivInfo

@accountRoutes.route('/api/updatePixivInfo', methods=['POST'])
def updatePixivInfo():
    dlCount = accountManager.getSingleData('dl_count')
    imagesCount = accountManager.getSingleData('images_count')
    pixivAccounts = accountManager.getSingleData('pixiv')
    
    data = request.get_json()
    imagesCount += int(data['imageCount'])
    dlCount += 1
    
    if data['getPostType'] == 'tag':
        isTagExists = False
        for (i, pixivAccount) in enumerate(pixivAccounts):
            if pixivAccount['tag'] == data['tag']:
                pixivAccounts[i]['post'] = str(data['latestID'])
                isIdExists = True
                
        if not isTagExists:
            pixivAccounts.append({
                'tag': data['tag'],
                'post': str(data['latestID']),
                'id': ''
            })
    else:
        isIdExists = False
        for (i, pixivAccount) in enumerate(pixivAccounts):
            if pixivAccount['id'] == str(data['pixUserID']):
                pixivAccounts[i]['post'] = str(data['latestID'])
                isIdExists = True
                
        if not isIdExists:
            pixivAccounts.append({
                'id': str(data['pixUserID']),
                'post': str(data['latestID']),
                'tag': ''
            })
        
    accountManager.update('dl_count', dlCount)
    accountManager.update('images_count', imagesCount)
    accountManager.update('pixiv', pixivAccounts)
    
    return 'success'

@accountRoutes.route('/api/getTwitterInfo', methods=['GET'])
def getTwitterInfo():
    twitterInfo = accountManager.getSingleData('twitter')
    return twitterInfo

@accountRoutes.route('/api/updateTwitterInfo', methods=['POST'])
def updateTwitterInfo():
    dlCount = accountManager.getSingleData('dl_count')
    imagesCount = accountManager.getSingleData('images_count')
    twitterAccounts = accountManager.getSingleData('twitter')
    
    data = request.get_json()
    imagesCount += int(data['imageCount'])
    dlCount += 1
    
    isIdExists = False
    for (i, twitterAccount) in enumerate(twitterAccounts):
        if twitterAccount['id'] == str(data['twitterID']):
            twitterAccounts[i]['post'] = str(data['latestID'])
            isIdExists = True
            
    if not isIdExists:
        twitterAccounts.append({
            'id': str(data['twitterID']),
            'post': str(data['latestID'])
        })
        
    accountManager.update('dl_count', dlCount)
    accountManager.update('images_count', imagesCount)
    accountManager.update('twitter', twitterAccounts)
    
    return 'success'