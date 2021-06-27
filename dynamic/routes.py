import flask
from dynamic import app


@app.route("/")
def home():
    return flask.render_template("home.html")
