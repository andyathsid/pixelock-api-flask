from flask import Flask
from flask_cors import CORS
from decouple import config
from app.routes.api import api

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Configure max content length
    app.config['MAX_CONTENT_LENGTH'] = int(config('MAX_CONTENT_LENGTH', default=5242880))
    
    app.register_blueprint(api, url_prefix='/api')
    
    return app

# Create the application instance
app = create_app()