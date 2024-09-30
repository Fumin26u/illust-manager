from flask import g

def to_dict(row):
    return {
        'id': row['id'],
        'user_platform_account_id': row['user_platform_account_id'],
        'post_id': row['post_id'],
        'filename': row['filename'],
        'downloaded_at': row['downloaded_at'].isoformat(),
        'delete_fg': row['delete_fg']
    }

def select(user_platform_account_id, limit=100):
    db = g.db
    cursor = db.cursor(dictionary=True)
    
    # サブクエリを作成して最新のdownloaded_atを取得
    subquery = '''
    SELECT MAX(downloaded_at)
    FROM user_platform_account_dl_log
    WHERE user_platform_account_id = %s
    '''
    
    cursor.execute(subquery, (user_platform_account_id,))
    max_downloaded_at = cursor.fetchone()['MAX(downloaded_at)']
    
    # メインクエリを実行して結果を取得
    sql = '''
    SELECT post_id
    FROM user_platform_account_dl_log
    WHERE user_platform_account_id = %s
    AND downloaded_at = %s
    ORDER BY downloaded_at DESC
    LIMIT %s
    '''
    
    cursor.execute(sql, (user_platform_account_id, max_downloaded_at, limit))
    results = cursor.fetchall()
    cursor.close()
    
    return results

def create(user_platform_account_id, post_id, downloaded_at):
    db = g.db
    cursor = db.cursor()
    
    sql = '''
    INSERT INTO user_platform_account_dl_log (user_platform_account_id, post_id, downloaded_at)
    VALUES (%s, %s, %s)
    '''
    
    cursor.execute(sql, (user_platform_account_id, post_id, downloaded_at))
    db.commit()
    
    user_platform_account_id = cursor.lastrowid
    cursor.close()
    
    return user_platform_account_id