from flask import Blueprint, request, session, jsonify, make_response
import os
from api.error.response import res_400, res_404
from api.service.user import getUser
import api.service.twitter.twitter

twitterController = Blueprint('twitterController', __name__)
basePath = '/api/twitter'

@twitterController.route(f"{basePath}/getTweet", methods=['GET'])
def getTweet():
    try:
        searchQuery = request.get_json()
        user = getUser(session['user_id'])
        tweets = api.service.twitter.twitter.getTweet(user, searchQuery)
        
        return res_404 if not tweets else jsonify(tweets), 200
    except Exception as e:
        return res_400(e)

@twitterController.route(f"{basePath}/download", methods=['POST'])
async def download():
    try:    
        query = request.get_json()
        if not query: 
            return res_400('No data provided')
        
        images = [query['illust']['images']['url'] for query in query['illust']['images']]
        post_ids = [query['illust']['postID'] for query in query['illust']]
        
        zipPath = api.service.twitter.twitter.download(images)
        if not zipPath:
            return res_400('Download failed')
                
        response = api.service.twitter.twitter.update(
            session['user_id'], 
            post_ids, 
            len(images)
        )
        
        response = make_response()
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = f'attachment; filename={os.path.basename(zipPath)}'
        response.data = open(zipPath, 'rb').read()
        
        return res_404 if not response else jsonify({'zip_path': zipPath}), 200
    except Exception as e:
        return res_400(e)