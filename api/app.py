from flask import Flask, request, jsonify, g
from flask_cors import CORS
from dotenv import load_dotenv
import os
from datetime import timedelta
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

from api.config.mysql import MYSQL_CONFIG
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}/{MYSQL_CONFIG['database']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=30)

from api.sqlAlchemy import db
db.init_app(app)

with app.app_context():
    from api.model import User
    from api.model import UserImage
    from api.model import UserImageTag
    from api.model import UserPlatformAccount
    from api.model import UserPlatformAccountDlLog
    
from api.controller.user import userController
from api.controller.twitter import twitterController
from api.controller.pixiv import pixivController
from api.controller.download import downloadController
from api.controller.userPlatformAccount import userPlatformAccountController
from api.controller.userPlatformAccountDlLog import userPlatformAccountDlLogController

app.register_blueprint(userController)
app.register_blueprint(twitterController)
app.register_blueprint(pixivController)
app.register_blueprint(downloadController)
app.register_blueprint(userPlatformAccountController)
app.register_blueprint(userPlatformAccountDlLogController)

from api.config.origin import ORIGIN
CORS(app, resources={r"/*": {"origins": ORIGIN}})

@app.before_request
def before_request():
    user_id = request.headers.get('user_id')
    if user_id:
        g.user_id = user_id
    else:
        g.user_id = None
        
if __name__ == '__main__':
    app.run(debug=True)