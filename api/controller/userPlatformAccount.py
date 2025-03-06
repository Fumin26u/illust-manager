from flask import Blueprint, request, jsonify, g

import api.service.userPlatformAccount
from api.error.response import res_400
import api.error.exception as exception

userPlatformAccountController = Blueprint('userPlatformAccount', __name__)
basePath = "/api/userPlatformAccount"

@userPlatformAccountController.route(f"{basePath}/update", methods=['POST'])
async def update():
    try:
        query = request.get_json()
        if not query: 
            raise exception.NoQueryProvidedException()
                
        userPlatformAccount = api.service.userPlatformAccount.select(g.user_id, query['platform'])
        dl_count = userPlatformAccount['dl_count'] + 1
        get_images_count = userPlatformAccount['get_images_count'] + int(query['get_images_count'])
        
        result = api.service.userPlatformAccount.update(userPlatformAccount['id'], dict(
            dl_count = dl_count,
            get_images_count = get_images_count,    
        ))
        if not result:
            raise Exception('INTERNAL SERVER ERROR: update userPlatForm is failed')
        
        return jsonify({'error': False, 'content': 'update done'}), 200
    except Exception as e:
        print(e)
        return res_400(e)
    
    