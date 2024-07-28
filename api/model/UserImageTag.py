from flask import g

def to_dict(row):
    return {
        'id': row['id'],
        'user_image_id': row['user_image_id'],
        'name_en': row['name_en'],
        'name_ja': row['name_ja'],
        'confidence': row['confidence'],
    }

def get_all():
    db = g.db
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM user_image_tag')
    user_image_tags = cursor.fetchall()
    cursor.close()
    db.close()
    return [to_dict(user_image_tag) for user_image_tag in user_image_tags]

def get(user_image_id: int):
    db = g.db
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM user_image_tag WHERE user_image_id = %s', (user_image_id,))
    user_image_tags = cursor.fetchall()
    cursor.close()
    return [to_dict(user_image_tag) for user_image_tag in user_image_tags]

def create(
    user_image_id: int,
    name_en: str,
    name_ja: str,
    confidence: str | float
):
    db = g.db
    cursor = db.cursor()
    sql = """
        INSERT INTO user_image_tag (user_image_id, name_en, name_ja, confidence)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (user_image_id, name_en, name_ja, confidence))
    db.commit()
    affected_rows = cursor.rowcount
    
    cursor.close()
    
    if affected_rows == 0:
        return False
    
    return True
