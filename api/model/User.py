import uuid
from datetime import datetime
from flask import g

def to_dict(row):
    return {
        'id': row['id'],
        'user_name': row['user_name'],
        'email': row['email'],
        'uuid': str(uuid.UUID(bytes=row['uuid'])),
        'created_at': row['created_at'].isoformat(),
        'updated_at': row['updated_at'].isoformat()
    }

def get(user_id: int):
    db = g.db
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM user WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()
    
    if not user:
        return False
    
    return to_dict(user)

def create(userInfo):
    db = g.db
    cursor = db.cursor()
    
    sql = '''
    INSERT INTO user (user_name, password, email, created_at, updated_at) 
    VALUES (%s, %s, %s, %s, %s)
    '''
    values = (
        userInfo['user_name'],
        userInfo['password'],
        userInfo['email'],
        datetime.now(),
        datetime.now()
    )
    
    cursor.execute(sql, values)
    db.commit()
    user_id = cursor.lastrowid
    
    cursor.close()
    
    return user_id

def update(user_id: int, userInfo):
    db = g.db
    cursor = db.cursor()
    
    # パスワードが存在しない場合は空文字列にする
    password = userInfo['password'] if 'password' in userInfo else ''
    
    sql = '''
    UPDATE user 
    SET user_name = %s, password = %s, email = %s, updated_at = %s 
    WHERE id = %s
    '''
    values = (
        userInfo['user_name'],
        password,
        userInfo['email'],
        datetime.now(),
        user_id
    )
    
    cursor.execute(sql, values)
    db.commit()
    affected_rows = cursor.rowcount
    
    cursor.close()
    
    if affected_rows == 0:
        return False
    
    return user_id
