import flask
from dynamic import app


@app.route("/")
def python_runner():
    return flask.render_template("python_runner.html")


@app.route("/js")
def js_runner():
    return flask.render_template("js_runner.html")
