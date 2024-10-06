from flask import jsonify

def res_400():
    return jsonify({'error': True, 'message': 'Bad Request'}), 400

def res_401():
    return jsonify({'error': True, 'message': 'Unauthorized'}), 401

def res_403():
    return jsonify({'error': True, 'message': 'Forbidden'}), 403

def res_404():
    return jsonify({'error': True, 'message': 'Not Found'}), 404

def res_405():
    return jsonify({'error': True, 'message': 'Method Not Allowed'}), 405

def res_500():
    return jsonify({'error': True, 'message': 'Internal Server Error'}), 500
