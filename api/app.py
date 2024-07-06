from flask import Flask
from flask_cors import CORS
from api.account.accountRoutes import accountRoutes
from api.imagedler.pixiv.pixivRoutes import pixivRoutes
from api.imagedler.twitter.twitterRoutes import twitterRoutes

from api.account.accountManager import AccountManager
from api.utils.createPath import createPath

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

app.register_blueprint(accountRoutes)
app.register_blueprint(pixivRoutes)
app.register_blueprint(twitterRoutes)

accountManager = AccountManager(createPath('account', 'userdata.json'))

@app.route('/', methods=['GET'])
def index():
    return 'This is an Index Page!'

if __name__ == '__main__':
    app.run(debug=True)
