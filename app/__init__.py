from flask import Flask
from config import Config

# import blueprints
from .auth.routes import auth

app = Flask(__name__)


# register blueprints
app.register_blueprint(auth)

app.config.from_object(Config)

from . import routes