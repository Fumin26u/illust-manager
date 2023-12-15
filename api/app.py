from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

@app.route('/', methods=['GET'])
def index():
    return 'This is an Index Page!'

@app.route('/api/getDirectory', methods=['GET'])
def get_directory():
    file = request.files.get('file')
    return jsonify({'directoryPath': file})
    # if file:
    #     # return jsonify({'directoryPath': os.path.dirname(file.filename)})
    # else:
    #     return jsonify({'error': 'File not found'}), 400

if __name__ == '__main__':
    app.run(debug=True)
