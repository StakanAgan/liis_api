from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def create_app(config_class=Config):
    app = Flask(__name__)
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')


from app import models