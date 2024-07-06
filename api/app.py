from flask import Flask, jsonify
from flask_cors import CORS

from api.config.origin import ORIGIN
from api.config.mysql import MYSQL_CONFIG

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": ORIGIN}})