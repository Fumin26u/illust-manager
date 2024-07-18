from flask import Blueprint, request, jsonify, g

import api.service.userPlatformAccountDlLog
import api.service.userPlatformAccount
from api.error.response import res_400, res_404
from datetime import datetime

userPlatformAccountDlLogController = Blueprint('userPlatformAccountDlLog', __name__)
basePath = "/api/userPlatformAccountDlLog"

@userPlatformAccountDlLogController.route(f"{basePath}/insert", methods=['POST'])
async def insert():
    try:
        query = request.get_json()
        if not query: 
            return res_400('No data provided')
        
        userPlatformAccount = api.service.userPlatformAccount.select(g.user_id, query['platform'])
        print(userPlatformAccount)
        
        for post_id in query['post_id']:
            api.service.userPlatformAccountDlLog.create(
                userPlatformAccount['id'],
                post_id,
                datetime.now()
            )
        
        return jsonify({'error': False, 'content': 'insert done'}), 200
    except Exception as e:
        return res_400(e)