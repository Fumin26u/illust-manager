from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from api.config.origin import ORIGIN

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

CORS(app, resources={r"/*": {"origins": ORIGIN}})