from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import config

api_blue_print = Blueprint('api', __name__, url_prefix='/api/v1')
#initialize the api class
api = Api(api_blue_print)
#initialize the database
db = SQLAlchemy()

def create_app(configuration):
    """
    This is the application factory depending on the configuratios passed
    e.g for testing environment
    It returns the the fully initialized application
    """
    app = Flask(__name__)
    app.config.from_object(config[configuration])
    db.init_app(app)
    app.register_blueprint(api_blue_print)
    return app
