#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Amenities"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
@swag_from('swagger_yaml/amenities_no_id.yml', methods=['GET', 'POST'])
def get_amenities():
    """
    Retrieves a list of all amenities
    """
    if request.method == 'GET':
        all_amenities = storage.all(Amenity).values()
        list_amenities = []
        for amenity in all_amenities:
            list_amenities.append(amenity.to_dict())
        return jsonify(list_amenities)

    if request.method == 'POST':
        if not request.get_json():
            abort(400, description="Not a JSON")

        if 'name' not in request.get_json():
            abort(400, description="Missing name")

        data = request.get_json()
        instance = Amenity(**data)
        instance.save()
        return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>/', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
@swag_from('swagger_yaml/amenities_id.yml', methods=['GET', 'DELETE', 'PUT'])
def get_amenity(amenity_id):
    """ Retrieves an amenity """
    if request.method == 'GET':
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)

        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        amenity = storage.get(Amenity, amenity_id)

        if not amenity:
            abort(404)

        storage.delete(amenity)
        storage.save()

        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, description="Not a JSON")

        ignore = ['id', 'created_at', 'updated_at']

        amenity = storage.get(Amenity, amenity_id)

        if not amenity:
            abort(404)

        data = request.get_json()
        for key, value in data.items():
            if key not in ignore:
                setattr(amenity, key, value)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
