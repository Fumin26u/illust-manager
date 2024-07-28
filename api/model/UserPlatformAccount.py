from flask import g

def to_dict(row):
    return {
        'id': row['id'],
        'user_id': row['user_id'],
        'platform': row['platform'],
        'platform_id': row['platform_id'],
        'platform_password': row['platform_password'],
        'dl_count': row['dl_count'],
        'get_images_count': row['get_images_count'],
        'created_at': row['created_at'].isoformat(),
        'updated_at': row['updated_at'].isoformat()
    }

def select(user_id, platform):
    db = g.db
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM user_platform_account WHERE user_id = %s AND platform = %s', (user_id, platform))
    account = cursor.fetchone()
    cursor.close()
    
    if not account:
        return None
    
    return to_dict(account)

def update(user_platform_account_id, args):
    db = g.db
    cursor = db.cursor()

    columns = ', '.join(f"{key} = %s" for key in args.keys())
    values = list(args.values())
    values.append(user_platform_account_id)
    
    sql = f"UPDATE user_platform_account SET {columns} WHERE id = %s"
    
    cursor.execute(sql, values)
    db.commit()
    affected_rows = cursor.rowcount
    
    cursor.close()
    
    if affected_rows == 0:
        return False
    
    return True