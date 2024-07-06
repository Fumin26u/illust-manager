from flask import jsonify
from api.model import db, User
from datetime import datetime

def getUser(user_id: int):
    try:
        user = User.query.filter_by(id = user_id).first()
        if not user: 
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({ 'error': True, 'content': str(e) }), 400

def createUser(userInfo): 
    try:
        new_user = User(
            user_name = userInfo['user_name'],
            password = userInfo['password'],
            email = userInfo['email'],
            uuid = userInfo['uuid'],
            created_at = datetime.now(),
            updated_at = datetime.now()
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'user_id': new_user.user_id}), 201
    except Exception as e:
        return jsonify({ 'error': True, 'content': str(e) }), 400
    
def updateUser(user_id: int, userInfo):    
    try:
        user = User.query.filter_by(id = user_id).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        if 'user_name' in userInfo:
            user.user_name = userInfo['user_name']
        if 'password' in userInfo:
            user.password = userInfo['password']
        if 'email' in userInfo:
            user.email = userInfo['email']
            
        user.updated_at = datetime.now()
        
        db.session.commit()
        
        return jsonify({'user_id': user.user_id}), 200
    except Exception as e:
        return jsonify({ 'error': True, 'content': str(e) }), 400