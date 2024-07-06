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

class UserImageTag(db.Model):
    __table__ = db.Table('user_image_tag', db.metadata, autoload_with=db.engine)

class UserPlatformAccount(db.Model):
    __table__ = db.Table('user_platform_account', db.metadata, autoload_with=db.engine)

class UserPlatformAccountDlLog(db.Model):
    __table__ = db.Table('user_platform_account_dl_log', db.metadata, autoload_with=db.engine)