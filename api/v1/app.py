#!/usr/bin/python3
"""AirBnB Clone API config file"""
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
from os import getenv
from flasgger import Swagger

app = Flask('__name__')
swagger = Swagger(app)

app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_app(exception):
    """ends a db session at the end of a request"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """handle non existing pages
    """
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(debug=True)
    app.run(host=host, port=port)
