from flask import jsonify

def res_400(e):
    return jsonify({'error': True, 'message': 'Bad Request'}), 400

def res_401(e):
    return jsonify({'error': True, 'message': 'Unauthorized'}), 401

def res_403(e):
    return jsonify({'error': True, 'message': 'Forbidden'}), 403

def res_404(e):
    return jsonify({'error': True, 'message': 'Not Found'}), 404

def res_405(e):
    return jsonify({'error': True, 'message': 'Method Not Allowed'}), 405

def res_500(e):
    return jsonify({'error': True, 'message': 'Internal Server Error'}), 500
