from flask import Blueprint, request, jsonify

from api.error.response import res_400, res_404
import api.service.download.image.main
import api.service.download.zip.downloadZip

downloadController = Blueprint('downloadController', __name__)
basePath = "/api/download"

@downloadController.route(f"{basePath}/image", methods=['POST'])
async def downloadImage():
    try:    
        query = request.get_json()
        if not query: 
            return res_400('No data provided')
        
        response = await api.service.download.image.main.download(query['images'], query['platform'])
        if response['error']:
            return res_400('Download failed')
                    
        return jsonify(response), 200
    except Exception as e:
        return res_400(e)
    
@downloadController.route(f"{basePath}/zip", methods=['GET'])
def downloadZip():
    try:
        timestamp = request.args.get('timestamp')
        platform = request.args.get('platform')
        
        if not timestamp:
            return res_400('No timestamp provided')
        if not platform:
            return res_400('No platform provided')
        
        response = api.service.download.zip.downloadZip.downloadZip(timestamp, platform)
        
        return res_404 if not response else response, 200
    except Exception as e:
        return res_400(e)
    
# ローカルからimportしたrawImageを取り込む
@downloadController.route(f"{basePath}/local/import", methods=['POST'])
async def importLocalImage():
    try:
        query = request.get_json()
        if not query['images']: 
            return res_400('No data provided')
                
        response = await api.service.download.image.main.download(query['images'], 'local')
        if response['error']:
            return res_400('Import failed')
                    
        return jsonify(response), 200
    except Exception as e:
        return res_400(e)