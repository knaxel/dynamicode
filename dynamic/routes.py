import flask
from dynamic import app


@app.route("/")
def python_runner():
    return flask.render_template("python_runner.html")
