import os
import api.service.image

from flask import Blueprint, request, jsonify, send_from_directory, g
from api.error.response import res_400, res_404
from api.utils.string import getRootDir

imageController = Blueprint('imageController', __name__)
basePath = "/api/image"

@imageController.route(f"{basePath}/directories", methods=['GET'])
def getDirectories():
    try:
        platform = request.args.get('platform')
        if not platform:
            return res_400('No platform provided')
        
        response = api.service.image.getDirectories(platform)
        
        return jsonify({'error': False, 'directories': response}), 200
    except Exception as e:
        return res_400(e)
    
@imageController.route(f"{basePath}/load", methods=['POST'])
def loadImages():
    try:
        query = request.get_json()
        if not query:
            return res_400('No data provided')
        
        response = api.service.image.loadImages(query['directory_name'], query['platform'])
        
        return jsonify({'error': False, 'images': response}), 200
    except Exception as e:
        return res_400(e)
    
@imageController.route(f"{basePath}/<platform>/<directory>/<filename>", methods=['GET'])
def getImage(platform, directory, filename):
    try:
        rootDir = getRootDir()
        targetImageDirPath = f"{rootDir}/downloads/{platform}/images/{directory}"
        if not os.path.exists(targetImageDirPath):
            return res_404('Image not found')
        
        return send_from_directory(targetImageDirPath, filename)
    except Exception as e:
        return res_400(e)
    
@imageController.route(f"{basePath}/tag/generate", methods=['POST'])
def generateTagsFromImage():
    try:
        query = request.get_json()
        images = query['images']
        if not images:        
            return res_400('必要な情報が提供されませんでした。')
        
        response = api.service.image.generateTagsFromImage(images, g.user_id)
        if not response:
            Exception('タグの生成に失敗しました。')
        
        return jsonify({'error': False, 'content': response}), 200
    except Exception as e:
        return res_400(e)
    
@imageController.route(f"{basePath}/save", methods=['POST'])
def saveImage():
    try:
        query = request.get_json()
        if not query:
            return res_400('No data provided')
        
        # 以下の順序で画像を保存する
        # 画像ファイルにタグを付与 (TODO:とりあえず信頼度上位10個)
        # 画像ファイルをimages/${Y-m-d_H-i-s}/${Y-m-d_H-i-s_${index}}.${extension}として保存
        # user_image, user_image_tagテーブルに画像情報をINSERT
        
        images = query['images']
        for (index, image) in enumerate(images):
            if (
                not image['tags'] or
                not image['platform'] or
                not image['directory'] or
                not image['name']
            ):
                return res_400('必要情報が提供されませんでした。')
            # response = api.service.image.addTagsToImage(imagePath, tags)
            newFilename = api.service.image.verifyImage(index, image)
            print(newFilename)
            response = api.service.image.saveImage(image, newFilename, g.user_id)
            
            if response['error']:
                return res_400(response['content'])
            
        
        return jsonify({'error': False, 'content': 'save success'}), 200
    except Exception as e:
        return res_400(e)