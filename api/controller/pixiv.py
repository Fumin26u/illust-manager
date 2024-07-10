from flask import Blueprint, request, session, jsonify, make_response

import api.service.pixiv.pixiv
import api.service.userPlatformAccount
from api.error.response import res_400, res_404

pixivController = Blueprint('pixivController', __name__)
platform = 'pixiv'
basePath = f"/api/{platform}"

@pixivController.route(f"{basePath}/<int:user_id>", methods=['GET'])
def getUserPlatformAccount(user_id):
    try:
        userPlatformAccount = api.service.userPlatformAccount.select(user_id, platform)
        return res_404 if not userPlatformAccount else jsonify(userPlatformAccount), 200
    except Exception as e:
        return res_400(e)

@pixivController.route(f"{basePath}/getPost/<int:user_id>", methods=['POST'])
async def getPost(user_id):
    try:
        searchQuery = request.get_json()
        illust = await api.service.pixiv.pixiv.getPost(user_id, searchQuery)
        return res_404 if not illust else jsonify(illust), 200
    except Exception as e:
        return res_400(e)

@pixivController.route(f"{basePath}/download/<int:user_id>", methods=['POST'])
async def download(user_id):
    try:
        query = request.get_json()
        if not query: 
            return res_400('No data provided')
        
        images = [image['url'] for illust in query['illust'] for image in illust['images']]
        post_ids = [illust['postID'] for illust in query['illust']]
        
        nowTime = await api.service.pixiv.pixiv.download(images)
        if not nowTime:
            return res_400('Download failed')
            
        response = api.service.pixiv.pixiv.update(
            user_id, 
            post_ids, 
            len(images)
        )
        
        return res_404 if not response else jsonify({'now_time': nowTime}), 200
    except Exception as e:
        return res_400(e)
    
@pixivController.route(f"{basePath}/downloadZip", methods=['GET'])
async def downloadZip():
    try:
        timestamp = request.args.get('timestamp')
        if not timestamp:
            return res_400('No timestamp provided')
        
        print (f"TIMESTAMP: {timestamp}")
        
        response = api.service.pixiv.pixiv.downloadZip(make_response(), timestamp)
        
        return res_404 if not response else response, 200
    except Exception as e:
        return res_400(e)