import flask
from flask_bootstrap import Bootstrap

app = flask.Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = "0278h2hd0and28dn3n82nud12n3fda31"

from dynamic import routes


def start(*args, **kwargs):
    app.run(*args, **kwargs)
