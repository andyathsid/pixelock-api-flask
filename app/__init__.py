from flask import Flask
import os
from app.routes.api import api

app = Flask(__name__)  
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
app.register_blueprint(api, url_prefix='/api')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])