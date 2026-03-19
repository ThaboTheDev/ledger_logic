from flask import Flask, jsonify
from database.manager import DatabaseManager

def create_app():
    app = Flask(__name__)
    
    from api.app import main_bp
    
    app.register_blueprint(main_bp, url_prefix='/api/v1')
    return app