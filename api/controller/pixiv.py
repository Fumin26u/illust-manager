from flask import Blueprint, request, session, jsonify, make_response

import api.service.pixiv.pixiv
from api.error.response import res_400, res_404

pixivController = Blueprint('pixivController', __name__)
basePath = '/api/pixiv'

@pixivController.route(f"{basePath}/getPost", methods=['GET'])
async def getPost():
    try:
        searchQuery = request.get_json()
        illust = api.service.pixiv.pixiv.getPost(session['user_id'], searchQuery)
        return res_404 if not illust else jsonify(illust), 200
    except Exception as e:
        return res_400(e)

@pixivController.route(f"{basePath}/download", methods=['POST'])
def download():
    try:
        query = request.get_json()
        if not query: 
            return res_400('No data provided')
        
        images = [query['illust']['images']['url'] for query in query['illust']['images']]
        post_ids = [query['illust']['postID'] for query in query['illust']]
        
        zipPath = api.service.pixiv.pixiv.download(images)
        if not zipPath:
            return res_400('Download failed')
            
        response = api.service.pixiv.pixiv.update(
            session['user_id'], 
            post_ids, 
            len(images)
        )
        
        return res_404 if not response else jsonify({'zip_path': zipPath}), 200
    except Exception as e:
        return res_400(e)