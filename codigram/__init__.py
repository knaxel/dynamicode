import os
import flask
import json
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

ENV_FILE = os.path.join(os.path.dirname(__file__), os.pardir, "env.json")

app = flask.Flask(__name__)

if os.path.exists(ENV_FILE):
    with open(ENV_FILE) as read_file:
        ENV = json.load(read_file)
else:
    ENV = os.environ

app.config["SECRET_KEY"] = ENV["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = ENV["SQLALCHEMY_DATABASE_URL"]

Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "secondary"

from codigram import routes
from codigram import models

from codigram.models import User


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(user_id)


def start(debug=False):
    app.run(host="0.0.0.0", port=5000, debug=debug)
