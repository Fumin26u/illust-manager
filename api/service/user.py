from api.model import db, User
from datetime import datetime

def getUser(user_id: int):
    user = User.query.filter_by(id = user_id).first()
    if not user: 
        return False
    
    return user.to_dict()

def createUser(userInfo): 
    new_user = User(
        user_name = userInfo['user_name'],
        password = userInfo['password'],
        email = userInfo['email'],
        created_at = datetime.now(),
        updated_at = datetime.now()
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return new_user.id
    
def updateUser(user_id: int, userInfo): 
    user = User.query.filter_by(id = user_id).first()
    if not user:
        return False
    
    (db.session
        .query(User)
        .filter_by(id = user_id)
        .update(dict(
            user_name = userInfo['user_name'],
            password = '' if 'password' not in userInfo else userInfo['password'],
            email = userInfo['email'],
            updated_at = datetime.now()
        ))
    )
    
    db.session.commit()
    
    return user_id