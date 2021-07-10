import flask
from codigram import app
# from dynamic.models import get_sample_post


@app.route("/login")
def login():
    return flask.redirect(flask.url_for("python_runner"))


@app.route("/")
def python_runner():
    return flask.render_template("python_runner.html")
