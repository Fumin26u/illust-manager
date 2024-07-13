from flask import jsonify

def res_400(e):
    return jsonify({'error': 'Bad Request', 'content': e}), 400

def res_401():
    return jsonify({'error': 'Unauthorized'}), 401

def res_402():
    return jsonify({'error': 'Payment Required'}), 402

def res_403():
    return jsonify({'error': 'Forbidden'}), 403

def res_404():
    return jsonify({'error': 'URL Not Found'}), 404

def res_405():
    return jsonify({'error': 'Method Not Allowed'}), 405

def res_500():
    return jsonify({'error': 'Internal Server Error'}), 500