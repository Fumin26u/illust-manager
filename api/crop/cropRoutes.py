from flask import Blueprint, request, jsonify

import os, base64, cv2, string, random, uuid
import numpy as np
import concurrent.futures

from api.utils.createPath import createPath

cropRoutes = Blueprint('cropRoutes', __name__)

@cropRoutes.route('/crop/cropImage', methods=['POST'])
def cropImage():
    data = request.get_json()
    images = data['imagePaths']