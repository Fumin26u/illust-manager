from flask import Blueprint, request, jsonify, g

import api.service.userPlatformAccountDlLog
import api.service.userPlatformAccount
import api.error.exception as exception
from api.error.response import res_400, res_404
from datetime import datetime

userPlatformAccountDlLogController = Blueprint('userPlatformAccountDlLog', __name__)
basePath = "/api/userPlatformAccountDlLog"

@userPlatformAccountDlLogController.route(f"{basePath}/insert", methods=['POST'])
async def insert():
    try:
        query = request.get_json()
        if not query: 
            raise exception.NoQueryProvidedException()
        
        userPlatformAccount = api.service.userPlatformAccount.select(g.user_id, query['platform'])
        if not userPlatformAccount:
            raise Exception('INTERNAL SERVER ERROR: userPlatformAccount is not given')
        
        for post_id in query['post_id']:
            result = api.service.userPlatformAccountDlLog.create(
                userPlatformAccount['id'],
                post_id,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
            
            if not result:
                raise Exception('INTERNAL SERVER ERROR: insert userPlatformAccountDlLog is failed')
        
        return jsonify({'error': False, 'content': 'insert done'}), 200
    except Exception as e:
        print(e)
        return res_400(e)