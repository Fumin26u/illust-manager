from flask import g

def to_dict(row):
    return {
        'id': row['id'],
        'category_master_id': row['category_master_id'],
        'name_en': row['name_en'],
        'name_ja': row['name_ja'],
        'is_deprecated': row['is_deprecated'],
    }
    
def select_all():
    db = g.db
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM category')
    categories = cursor.fetchall()
    cursor.close()
    
    if not categories:
        return False
    
    return [to_dict(category) for category in categories]

def select(category_id: int):
    db = g.db
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM category WHERE id = %s', (category_id,))
    category = cursor.fetchone()
    cursor.close()
    
    if not category:
        return False
    
    return to_dict(category)