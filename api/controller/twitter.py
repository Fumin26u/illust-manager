from flask import Blueprint, request, jsonify, g

from api.error.response import res_400, res_404
import api.service.twitter.main
import api.service.userPlatformAccount

twitterController = Blueprint('twitterController', __name__)
platform = 'twitter'
basePath = f"/api/{platform}"

@twitterController.route(f"{basePath}", methods=['GET'])
def getUserPlatformAccount():
    try:
        userPlatformAccount = api.service.userPlatformAccount.select(g.user_id, platform)
        return res_404 if not userPlatformAccount else jsonify(userPlatformAccount), 200
    except Exception as e:
        return res_400(e)

@twitterController.route(f"{basePath}/getPost", methods=['POST'])
def getPost():
    try:
        searchQuery = request.get_json()
        tweets = api.service.twitter.main.getTweet(g.user_id, searchQuery)
        
        return res_404 if not tweets else jsonify(tweets), 200
    except Exception as e:
        return res_400(e)