from flask import Blueprint, request, jsonify, g

from api.error.response import res_400, res_404
import api.service.twitter.main
import api.service.userPlatformAccount
import api.error.exception as exception
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

twitterController = Blueprint('twitterController', __name__)
platform = 'twitter'
basePath = f"/api/{platform}"

@twitterController.route(f"{basePath}", methods=['GET'])
def getUserPlatformAccount():
    try:
        userPlatformAccount = api.service.userPlatformAccount.select(g.user_id, platform)
        if not userPlatformAccount:
            raise Exception('INTERNAL SERVER ERROR: userPlatformAccount is not given')
        
        return jsonify(userPlatformAccount), 200
    except Exception as e:
        print(e)
        return res_400(e)

@twitterController.route(f"{basePath}/getPost", methods=['POST'])
def getPost():
    try:
        query = request.get_json()
        if not query:
            raise exception.NoQueryProvidedException()
        
        tweets = api.service.twitter.main.getTweet(g.user_id, query)
        if not tweets:
            raise Exception('INTERNAL SERVER ERROR: ツイートを取得できませんでした')
        
        return res_404 if not tweets else jsonify(tweets), 200
    except Exception as e:
        logger.debug(e)
        return res_400(e)