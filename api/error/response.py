from flask import jsonify

def res_400(e):
    return jsonify({'error': True, 'content': e}), 400

def res_401():
    return jsonify({'error': True}), 401

def res_402():
    return jsonify({'error': True}), 402

def res_403():
    return jsonify({'error': True}), 403

def res_404():
    return jsonify({'error': True}), 404

def res_405():
    return jsonify({'error': True}), 405

def res_500():
    return jsonify({'error': True}), 500