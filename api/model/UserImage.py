import uuid
from api.db.connect import connect_db

class UserImage:
    @staticmethod
    def to_dict(row):
        return {
            'id': row['id'],
            'user_id': row['user_id'],
            'filename': row['filename'],
            'delete_fg': row['delete_fg'],
            'created_at': row['created_at'].isoformat(),
            'updated_at': row['updated_at'].isoformat()
        }

    @staticmethod
    def get_all():
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user_image')
        user_images = cursor.fetchall()
        cursor.close()
        db.close()
        return [UserImage.to_dict(user_image) for user_image in user_images]
