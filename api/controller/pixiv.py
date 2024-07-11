from flask import Blueprint, request, jsonify, make_response

import api.service.pixiv.main
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
        illust = await api.service.pixiv.main.getPost(user_id, searchQuery)
        return res_404 if not illust else jsonify(illust), 200
    except Exception as e:
        return res_400(e)