from api.controller.user import userController
from api.controller.twitter import twitterController
from api.controller.pixiv import pixivController
from api.app import app

app.register_blueprint(userController)
app.register_blueprint(twitterController)
app.register_blueprint(pixivController)

@app.route('/', methods=['GET'])
def index():
    return 'This is an Index Page!'

if __name__ == '__main__':
    app.run(debug=True)
