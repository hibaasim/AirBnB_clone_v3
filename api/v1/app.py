#!/usr/bin/python3
""" app for api """

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(*args):
    """ handles @app.teardown_appcontext """
    storage.close()


<<<<<<< HEAD
<<<<<<< HEAD
@app.errorhandler(404)
=======
@app.errorhandler(404)
>>>>>>> 9c47779976190391dce236b97aa8156ee7069a35
=======
@app.errorhandler(404)
>>>>>>> 4b745ae419fcc53c223dcbb944d027140b9914ef
def handle_error(*args):
    """"handles 404 errors"""
    return jsonify({"error": "Not found"})


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
