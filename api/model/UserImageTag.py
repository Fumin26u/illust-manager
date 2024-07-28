import uuid
from api.db.connect import connect_db

class UserImageTag:
    @staticmethod
    def to_dict(row):
        return {
            'id': row['id'],
            'user_image_id': row['user_image_id'],
            'tag_name': row['tag_name'],
            'tag_name_jp': row['tag_name_jp'],
            'confidence': row['confidence'],
        }

    @staticmethod
    def get_all():
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM user_image_tag')
        user_image_tags = cursor.fetchall()
        cursor.close()
        db.close()
        return [UserImageTag.to_dict(user_image_tag) for user_image_tag in user_image_tags]
