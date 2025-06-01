from flask import Flask
from app.core.config import Config

def create_app():
    app = Flask(__name__)
    Config.init_app(app)
    
    from app.views import main
    app.register_blueprint(main)
    
    return app