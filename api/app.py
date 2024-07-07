from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    
    from api.config.mysql import MYSQL_CONFIG
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}/{MYSQL_CONFIG['database']}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
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

    app.register_blueprint(userController)
    app.register_blueprint(twitterController)
    app.register_blueprint(pixivController)

    from api.config.origin import ORIGIN
    CORS(app, resources={r"/*": {"origins": ORIGIN}})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)