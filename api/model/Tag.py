from flask import g

def to_dict(row):
    return {
        'id': row['id'],
        'name_en': row['name_en'],
        'name_ja': row['name_ja'],
        'category_id': row['category_id'],
        'post_count': row['post_count'],
        'is_deprecated': row['is_deprecated'],
        'created_at': row['created_at'].isoformat(),
        'updated_at': row['updated_at'].isoformat()
    }
    
def select_all():
    db = g.db
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tag')
    tags = cursor.fetchall()
    cursor.close()
    
    if not tags:
        return False
    
    return [to_dict(tag) for tag in tags]
    
def select(tag_id: int):
    db = g.db
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT id, name_en FROM tag WHERE id = %s', (tag_id,))
    tag = cursor.fetchone()
    cursor.close()
    
    if not tag:
        return False
    
    return to_dict(tag)

def selectWithSearch(search: str):
    db = g.db
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tag WHERE name_en LIKE %s', ('%' + search + '%',))
    tags = cursor.fetchall()
    cursor.close()
    
    if not tags:
        return False
    
    return [to_dict(tag) for tag in tags]