from flask import Blueprint, request, jsonify

import api.service.userPlatformAccount
from api.error.response import res_400, res_404

userPlatformAccountController = Blueprint('userPlatformAccount', __name__)
basePath = "/api/userPlatformAccount"

@userPlatformAccountController.route(f"{basePath}/update/<int:user_id>", methods=['POST'])
async def update(user_id):
    try:
        query = request.get_json()
        if not query: 
            return res_400('No data provided')
        
        userPlatformAccount = api.service.userPlatformAccount.select(user_id, query['platform'])
        
        api.service.userPlatformAccount.update(userPlatformAccount['id'], dict(
            dl_count = userPlatformAccount['dl_count'] + 1,
            get_images_count = userPlatformAccount['get_images_count'] + int(query['get_images_count']),    
        ))
        return jsonify({'error': False, 'content': 'update done'}), 200
    except Exception as e:
        return res_400(e)
    
    