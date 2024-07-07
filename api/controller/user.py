from flask import Blueprint, request, session, jsonify
import api.service.user
from api.error.response import res_400, res_404

userController = Blueprint('userController', __name__)
basePath = '/api/user'

@userController.route(f"{basePath}/<int:user_id>", methods=['GET'])
def index(user_id):
    try:
        user = api.service.user.getUser(user_id)
        
        session['user_id'] = user_id
        print(session)
        
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