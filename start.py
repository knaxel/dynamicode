import os
from codigram import start, app


if __name__ == '__main__':
    debug = os.environ.get("PRODUCTION") != "True"
    start(debug=debug)
