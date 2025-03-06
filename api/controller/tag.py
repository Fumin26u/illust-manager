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
        return res_400(e)
    
@tagController.route(f"{basePath}/category", methods=['GET'])
def getTagsByCategory():
    try:
        categoryId = request.args.get('category_id')
        if not categoryId:
            raise exception.NoQueryProvidedException()
        
        tags = api.service.tag.selectByCategory(categoryId)
        if not tags:
            raise Exception('INTERNAL SERVER ERROR: tags are not detected')
        
        return jsonify(tags), 200
    except Exception as e:
        print(e)
        return res_400(e)
    
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
        return res_400(e)
        
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
        return res_400(e)
    
@tagController.route(f"{basePath}/update/cluster", methods=['PUT'])
def updateCluster():
    try:
        query = request.json
        if (
            not query or 
            not query['tags'] or
            not query['category_id']
        ):
            raise exception.NoQueryProvidedException()
        
        tags = query['tags']
        categoryId = query['category_id']
        
        result = []
        for tag in tags:
            result.append(api.service.tag.update({
                'id': tag['id'],
                'name_ja': tag['name_ja'],
                'category_id': categoryId
            }))
        if not result:
            raise Exception('INTERNAL SERVER ERROR')
        
        return jsonify(result), 200
    except Exception as e:
        print(e)
        return res_400(e)