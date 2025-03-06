from flask import Blueprint, request, jsonify, g

import api.service.pixiv.main
import api.service.userPlatformAccount
from api.error.response import res_400

pixivController = Blueprint('pixivController', __name__)
platform = 'pixiv'
basePath = f"/api/{platform}"

@pixivController.route(f"{basePath}", methods=['GET'])
def getUserPlatformAccount():
    try:
        userPlatformAccount = api.service.userPlatformAccount.select(g.user_id, platform)
        if not userPlatformAccount:
            raise Exception('INTERNAL SERVER ERROR: userPlatformAccount is not detected')
        
        return jsonify(userPlatformAccount), 200
    except Exception as e:
        print(e)
        return res_400(e)

@pixivController.route(f"{basePath}/getPost", methods=['POST'])
async def getPost():
    try:
        searchQuery = request.get_json()
        illust = await api.service.pixiv.main.getPost(g.user_id, searchQuery)
        if not illust:
            raise Exception('INTERNAL SERVER ERROR: 画像を取得できませんでした')
        
        return jsonify(illust), 200
    except Exception as e:
        print(e)
        return res_400(e)