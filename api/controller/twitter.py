from flask import Blueprint, request, jsonify, make_response
from api.error.response import res_400, res_404
import api.service.twitter.twitter

twitterController = Blueprint('twitterController', __name__)
basePath = '/api/twitter'

@twitterController.route(f"{basePath}/<int:user_id>", methods=['GET'])
def getUserPlatformAccount(user_id):
    try:
        userPlatformAccount = api.service.twitter.twitter.getUserPlatformAccount(user_id)
        return res_404 if not userPlatformAccount else jsonify(userPlatformAccount), 200
    except Exception as e:
        return res_400(e)

@twitterController.route(f"{basePath}/getTweet/<int:user_id>", methods=['POST'])
def getTweet(user_id):
    try:
        searchQuery = request.get_json()
        
        tweets = api.service.twitter.twitter.getTweet(user_id, searchQuery)
        
        return res_404 if not tweets else jsonify(tweets), 200
    except Exception as e:
        return res_400(e)

@twitterController.route(f"{basePath}/download", methods=['POST'])
async def download():
    try:    
        query = request.get_json()
        if not query: 
            return res_400('No data provided')
        
        images = [image['url'] for tweet in query['tweet'] for image in tweet['images']][::-1]
        post_ids = [tweet['postID'] for tweet in query['tweet']][::-1]
        
        nowTime = await api.service.twitter.twitter.download(images)
        if not nowTime:
            return res_400('Download failed')
                
        response = api.service.twitter.twitter.update(
            1, 
            post_ids, 
            len(images)
        )
        
        return res_404 if not response else jsonify({'zip_path': nowTime}), 200
    except Exception as e:
        return res_400(e)
    
@twitterController.route(f"{basePath}/downloadZip", methods=['GET'])
async def downloadZip():
    try:
        timestamp = request.args.get('timestamp')
        if not timestamp:
            return res_400('No timestamp provided')
        
        print (f"TIMESTAMP: {timestamp}")
        
        response = api.service.twitter.twitter.downloadZip(make_response(), timestamp)
        
        return res_404 if not response else response, 200
    except Exception as e:
        return res_400(e)