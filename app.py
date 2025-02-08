from flask import Flask, request, g
from flask_cors import CORS
from dotenv import load_dotenv
import os
import api.db.connect

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

from api.controller.user import userController
from api.controller.twitter import twitterController
from api.controller.pixiv import pixivController
from api.controller.download import downloadController
from api.controller.userPlatformAccount import userPlatformAccountController
from api.controller.userPlatformAccountDlLog import userPlatformAccountDlLogController
from api.controller.image import imageController
from api.controller.tag import tagController
from api.controller.category import categoryController

app.register_blueprint(userController)
app.register_blueprint(twitterController)
app.register_blueprint(pixivController)
app.register_blueprint(downloadController)
app.register_blueprint(userPlatformAccountController)
app.register_blueprint(userPlatformAccountDlLogController)
app.register_blueprint(imageController)
app.register_blueprint(tagController)
app.register_blueprint(categoryController)

from api.config.origin import ORIGIN
CORS(app, resources={r"/*": {"origins": ORIGIN}})

@app.before_request
def before_request():
    user_id = request.headers.get('user-id')
    g.db = api.db.connect.connect_db()
    if user_id:
        g.user_id = user_id
    else:
        g.user_id = None
        
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        
def get_db():
    if 'db' not in g:
        g.db = api.db.connect.connect_db()
    return g.db

import api.error.response as error_handler
app.register_error_handler(400, error_handler.res_400)
app.register_error_handler(401, error_handler.res_401)
app.register_error_handler(403, error_handler.res_403)
app.register_error_handler(404, error_handler.res_404)
app.register_error_handler(405, error_handler.res_405)
app.register_error_handler(500, error_handler.res_500)

if __name__ == '__main__':
    app.run(debug=True)