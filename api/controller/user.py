from flask import Blueprint, request, session, jsonify
import api.service.user
from api.error.response import res_400, res_404

userController = Blueprint('userController', __name__)
basePath = '/api/user'

@userController.route(f"{basePath}/<int:user_id>", methods=['GET'])
def index(user_id):
    try:
        user = api.service.user.getUser(user_id)
        return res_404 if not user else jsonify(user), 200
    except Exception as e:
        return res_400(e)
    
@userController.route(f"{basePath}", methods=['POST'])
def create():
    try:
        userInfo = request.get_json()
        user_id = api.service.user.createUser(userInfo)
        return jsonify({'user_id': user_id}), 200
    except Exception as e:
        return res_400(e)
    
@userController.route(f"{basePath}/<int:user_id>", methods=['PUT'])
def update(user_id):
    try:
        userInfo = request.get_json()
        if not userInfo: 
            return res_400('No data provided')
        
        user_id = api.service.user.updateUser(user_id, userInfo)
        return res_404 if not user_id else jsonify({'user_id': user_id}), 200
    except Exception as e:
        return res_400(e)

# @userController.route('/api/getPixivInfo', methods=['GET'])
# def getPixivInfo():
#     try:
#         pixivInfo = accountManager.getSingleData('pixiv')
#         return {'error': False, 'content': pixivInfo}
#     except Exception as e:  
#         return {'error': True, 'content': str(e)}

# @userController.route('/api/updateUserInfo', methods=['POST'])
# def updateUserInfo():
#     data = request.get_json()
#     try:
#         created_at = accountManager.getSingleData('created_at')
#         if created_at == None or created_at == '':
#             accountManager.update('created_at', datetime.now())
            
#         accountManager.update('updated_at', datetime.now())
#         accountManager.update('user_name', data['user_name'])
#         accountManager.update('twitter_password', data['twitter_password'])
#         accountManager.update('pixiv_password', data['pixiv_password'])
        
#         return {'error': False, 'content': 'success'}
#     except Exception as e:
#         return {'error': True, 'content': str(e)}
    
# @userController.route('/api/deleteUserInfo', methods=['POST'])
# def deleteUserInfo():
#     try:
#         accountManager.delete()
        
#         return {'error': False, 'content': 'success'}
#     except Exception as e:
#         return {'error': True, 'content': str(e)}

# @userController.route('/api/updatePixivInfo', methods=['POST'])
# def updatePixivInfo():
#     dlCount = accountManager.getSingleData('dl_count')
#     imagesCount = accountManager.getSingleData('images_count')
#     pixivAccounts = accountManager.getSingleData('pixiv')
    
#     data = request.get_json()
#     imagesCount += int(data['imageCount'])
#     dlCount += 1
    
#     if data['getPostType'] == 'tag':
#         isTagExists = False
#         for (i, pixivAccount) in enumerate(pixivAccounts):
#             if pixivAccount['tag'] == data['tag']:
#                 pixivAccounts[i]['post'] = str(data['latestID'])
#                 isIdExists = True
                
#         if not isTagExists:
#             pixivAccounts.append({
#                 'tag': data['tag'],
#                 'post': str(data['latestID']),
#                 'id': ''
#             })
#     else:
#         isIdExists = False
#         for (i, pixivAccount) in enumerate(pixivAccounts):
#             if pixivAccount['id'] == str(data['pixUserID']):
#                 pixivAccounts[i]['post'] = str(data['latestID'])
#                 isIdExists = True
                
#         if not isIdExists:
#             pixivAccounts.append({
#                 'id': str(data['pixUserID']),
#                 'post': str(data['latestID']),
#                 'tag': ''
#             })
        
#     accountManager.update('dl_count', dlCount)
#     accountManager.update('images_count', imagesCount)
#     accountManager.update('pixiv', pixivAccounts)
    
#     return 'success'

# @userController.route('/api/getTwitterInfo', methods=['GET'])
# def getTwitterInfo():
#     twitterInfo = accountManager.getSingleData('twitter')
#     return twitterInfo

# @userController.route('/api/updateTwitterInfo', methods=['POST'])
# def updateTwitterInfo():
#     dlCount = accountManager.getSingleData('dl_count')
#     imagesCount = accountManager.getSingleData('images_count')
#     twitterAccounts = accountManager.getSingleData('twitter')
    
#     data = request.get_json()
#     imagesCount += int(data['imageCount'])
#     dlCount += 1
    
#     isIdExists = False
#     for (i, twitterAccount) in enumerate(twitterAccounts):
#         if twitterAccount['id'] == str(data['twitterID']):
#             twitterAccounts[i]['post'] = str(data['latestID'])
#             isIdExists = True
            
#     if not isIdExists:
#         twitterAccounts.append({
#             'id': str(data['twitterID']),
#             'post': str(data['latestID'])
#         })
        
#     accountManager.update('dl_count', dlCount)
#     accountManager.update('images_count', imagesCount)
#     accountManager.update('twitter', twitterAccounts)
    
#     return 'success'