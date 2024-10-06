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
    cursor.execute('SELECT * FROM tag WHERE id = %s', (tag_id,))
    tag = cursor.fetchone()
    cursor.close()
    
    if not tag:
        return False
    
    return to_dict(tag)

def selectByCategory(category_id: int):
    db = g.db
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tag WHERE category_id = %s', (category_id,))
    tags = cursor.fetchall()
    cursor.close()
    
    if not tags:
        return False
    
    return [to_dict(tag) for tag in tags]

def selectWithSearch(search: str):
    db = g.db
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tag WHERE name_en LIKE %s', ('%' + search + '%',))
    tags = cursor.fetchall()
    cursor.close()
    
    if not tags:
        return False
    
    return [to_dict(tag) for tag in tags]

def selectTagWords(tag_id: int):
    db = g.db
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM tag_words WHERE tag_id = %s', (tag_id,))
    tag_words = cursor.fetchall()
    cursor.close()
    
    if not tag_words:
        return []
    
    return tag_words

def update(params):
    db = g.db
    
    sql = '''
    UPDATE tag
    SET name_ja = %s, category_id = %s
    WHERE id = %s
    '''
    
    cursor = db.cursor(dictionary=True)
    cursor.execute(sql, (params['name_ja'], params['category_id'], params['id']))
    db.commit()
    tag = select(params['id'])
    cursor.close()
    
    return tag