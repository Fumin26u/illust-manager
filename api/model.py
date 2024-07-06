from flask_sqlalchemy import SQLAlchemy
from api.app import app
from api.config.mysql import MYSQL_CONFIG

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}/{MYSQL_CONFIG['database']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __table__ = db.Table('user', db.metadata, autoload_with=db.engine)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'email': self.email,
            'uuid': self.uuid,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class UserImage(db.Model):
    __table__ = db.Table('user_image', db.metadata, autoload_with=db.engine)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'delete_fg': self.delete_fg,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class UserImageTag(db.Model):
    __table__ = db.Table('user_image_tag', db.metadata, autoload_with=db.engine)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_image_id': self.user_image_id,
            'tag_name': self.tag_name,
            'tag_name_jp': self.tag_name_jp,
        }

class UserPlatformAccount(db.Model):
    __table__ = db.Table('user_platform_account', db.metadata, autoload_with=db.engine)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'platform': self.platform,
            'platform_id': self.platform_id,
            'platform_password': self.platform_password,
            'dl_count': self.dl_count,
            'get_images_count': self.images_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        

class UserPlatformAccountDlLog(db.Model):
    __table__ = db.Table('user_platform_account_dl_log', db.metadata, autoload_with=db.engine)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_platform_account_id': self.user_platform_account_id,
            'post_id': self.post_id,
            'filename': self.filename,
            'downloaded_at': self.downloaded_at.isoformat(),
            'delete_fg': self.delete_fg
        }