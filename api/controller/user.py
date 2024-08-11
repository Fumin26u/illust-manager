from flask import Blueprint, request, jsonify, g
import api.service.user
from api.error.response import res_400
import api.error.exception as exception

userController = Blueprint('userController', __name__)
basePath = '/api/user'

@userController.route(f"{basePath}", methods=['GET'])
def index():
    try:
        user = api.service.user.getUser(g.user_id)
        if not user:
            raise Exception('INTERNAL SERVER ERROR: user is not detected')
        
        return jsonify(user), 200
    except Exception as e:
        print(e)
        return res_400()
    
@userController.route(f"{basePath}", methods=['POST'])
def create():
    try:
        userInfo = request.get_json()
        user_id = api.service.user.createUser(userInfo)
        return jsonify({'user_id': user_id}), 200
    except Exception as e:
        print(e)
        return res_400()
    
@userController.route(f"{basePath}/<int:user_id>", methods=['PUT'])
def update(user_id):
    try:
        userInfo = request.get_json()
        if not userInfo: 
            exception.NoUserInfoProvidedException()
        
        user_id = api.service.user.updateUser(g.user_id, userInfo)
        if not user_id:
            raise Exception('INTERNAL SERVER ERROR: ユーザ情報の更新に失敗しました')
        
        return jsonify({'user_id': user_id}), 200
    except Exception as e:
        print(e)
        return res_400()