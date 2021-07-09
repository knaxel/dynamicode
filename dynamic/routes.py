import flask
from dynamic import app
from dynamic.models import get_sample_post


@app.route("/")
def python_runner():
    return flask.render_template("python_runner.html", post=get_sample_post())
