import os
import flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = flask.Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = "0278h2hd0and28dn3n82nud12n3fda31"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URL"]
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "secondary"

from codigram import routes
from codigram import models


def start(debug=False):
    app.run(host="0.0.0.0", port=5000, debug=debug)
