from flask import Blueprint, request, jsonify

from api.error.response import res_400, res_404
import api.error.exception as exception
import api.service.download.image.main
import api.service.download.zip.downloadZip


downloadController = Blueprint('downloadController', __name__)
basePath = "/api/download"

@downloadController.route(f"{basePath}/image", methods=['POST'])
async def downloadImage():
    try:    
        query = request.get_json()
        if not query: 
            raise exception.NoParamsProvidedException()
        
        response = await api.service.download.image.main.download(query['images'], query['platform'])
        if response['error']:
            raise Exception('INTERNAL SERVER ERROR')
                    
        return jsonify(response), 200
    except Exception as e:
        print(e)
        return res_400(e)
    
@downloadController.route(f"{basePath}/zip", methods=['GET'])
def downloadZip():
    try:
        timestamp = request.args.get('timestamp')
        platform = request.args.get('platform')
        
        if not timestamp:
            raise exception.NoTimestampProvidedException()
        if not platform:
            raise exception.NoPlatformProvidedException()
        
        response = api.service.download.zip.downloadZip.downloadZip(timestamp, platform)
        
        return res_404 if not response else response, 200
    except Exception as e:
        print(e)
        return res_400(e)
    
# ローカルからimportしたrawImageを取り込む
@downloadController.route(f"{basePath}/local/import", methods=['POST'])
async def importLocalImage():
    try:
        query = request.get_json()
        if not query['images']: 
            raise exception.NoImageProvidedException()
                
        response = await api.service.download.image.main.download(query['images'], 'local')
        if response['error']:
            raise Exception('INTERNAL SERVER ERROR')
                    
        return jsonify(response), 200
    except Exception as e:
        print(e)
        return res_400(e)