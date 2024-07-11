from flask import Blueprint, request, jsonify

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
        
        user_id = query['user_id']
        userPlatformAccount = api.service.userPlatformAccount.select(user_id, query['platform'])
        
        for post_id in query['post_id']:
            response = api.service.userPlatformAccountDlLog.create(
                userPlatformAccount['id'],
                post_id,
                datetime.now()
            )
        
        return res_404 if not response else jsonify(response), 200
    except Exception as e:
        return res_400(e)