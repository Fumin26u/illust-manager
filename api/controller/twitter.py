from flask import Blueprint, request, jsonify, make_response

from api.error.response import res_400, res_404
import api.service.twitter.main
import api.service.userPlatformAccount

twitterController = Blueprint('twitterController', __name__)
platform = 'twitter'
basePath = f"/api/{platform}"

@twitterController.route(f"{basePath}/<int:user_id>", methods=['GET'])
def getUserPlatformAccount(user_id):
    try:
        userPlatformAccount = api.service.userPlatformAccount.select(user_id, platform)
        return res_404 if not userPlatformAccount else jsonify(userPlatformAccount), 200
    except Exception as e:
        return res_400(e)

@twitterController.route(f"{basePath}/getPost/<int:user_id>", methods=['POST'])
def getPost(user_id):
    try:
        searchQuery = request.get_json()
        tweets = api.service.twitter.main.getTweet(user_id, searchQuery)
        
        return res_404 if not tweets else jsonify(tweets), 200
    except Exception as e:
        return res_400(e)