from flask import Blueprint, request, jsonify, g
import api.service.category
from api.error.response import res_400
import api.error.exception as exception

categoryController = Blueprint('categoryController', __name__)
basePath = '/api/category'

@categoryController.route(f"{basePath}", methods=['GET'])
def index():
    try:
        categories = api.service.category.select_all()
        if not categories:
            raise Exception('INTERNAL SERVER ERROR: categories are not detected')
        
        return jsonify(categories), 200
    except Exception as e:
        print(e)
        return res_400(e)
