from flask import Blueprint, request, jsonify, g

import api.service.tag
from api.error.response import res_400
import api.error.exception as exception

tagController = Blueprint('tagController', __name__)
basePath = '/api/tag'

@tagController.route(f"{basePath}", methods=['GET'])
def index():
    try:
        tags = api.service.tag.select_all()
        if not tags:
            raise Exception('INTERNAL SERVER ERROR: tags are not detected')
        
        return jsonify(tags), 200
    except Exception as e:
        print(e)
        return res_400()
    
@tagController.route(f"{basePath}/search", methods=['GET'])
def search():
    try:
        query = request.args.get('query')
        
        tags = api.service.tag.selectWithSearch(query) if query else api.service.tag.select_all()
        if not tags:
            raise Exception('INTERNAL SERVER ERROR: tags are not detected')
        
        return jsonify(tags), 200
    except Exception as e:
        print(e)
        return res_400()
        
@tagController.route(f"{basePath}/update", methods=['PUT'])
def update():
    try:
        query = request.json
        if not query:
            raise exception.NoQueryProvidedException()
        
        tag = api.service.tag.update(query)
        if not tag:
            raise Exception('INTERNAL SERVER ERROR')
        
        return jsonify(tag), 200
    except Exception as e:
        print(e)
        return res_400()