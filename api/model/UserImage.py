from flask import g

def to_dict(row):
    return {
        'id': row['id'],
        'user_id': row['user_id'],
        'filename': row['filename'],
        'delete_fg': row['delete_fg'],
        'created_at': row['created_at'].isoformat(),
        'updated_at': row['updated_at'].isoformat()
    }

def get_all():
    db = g.db
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM user_image')
    user_images = cursor.fetchall()
    cursor.close()
    db.close()
    
    if not user_images:
        return None
    
    return [to_dict(user_image) for user_image in user_images]
    
def get(user_id: int):
    db = g.db
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM user_image WHERE user_id = %s', (user_id,))
    user_images = cursor.fetchone()
    cursor.close()
    
    return [to_dict(user_image) for user_image in user_images]

def create(
    user_id: int,
    filename: str,
    delete_fg: bool,
    created_at: str,
    updated_at: str
):
    db = g.db
    cursor = db.cursor()
    
    sql = """
        INSERT INTO user_image (user_id, filename, delete_fg, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (user_id, filename, delete_fg, created_at, updated_at))
    db.commit()
    user_image_id = cursor.lastrowid
    
    cursor.close()
    
    if user_image_id == 0:
        return False
    
    return user_image_id
    
