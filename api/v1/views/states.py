#!/usr/bin/python3
"""Comment
"""
from models.state import State
from models import storage
from api.v1.views import app_views
from flasgger import Swagger, swag_from
from flask import abort, jsonify, make_response, request


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@swag_from('swagger_yaml/states_no_id.yml', methods=['GET', 'POST'])
def all_states():
    """Comment
    """
    if request.method == 'GET':
        all_states = storage.all(State).values()
        state_list = []

        for state in all_states:
            state_list.append(state.to_dict())

        return jsonify(state_list), 200

    if request.method == 'POST':
        if request.get_json:
            kwargs = request.get_json()
        else:
            return "Not a JSON", 400

        if kwargs:
            if 'name' not in kwargs.keys():
                return 'Missing name', 400

        try:
            state = State(**kwargs)
            state.save()
        except TypeError:
            return "Not a JSON", 400

        return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
@swag_from('swagger_yaml/states_id.yml', methods=['PUT', 'GET', 'DELETE'])
def get_state(state_id=None):
    """Comment
    """
    if request.method == 'GET':
        if state_id is None:
            abort(404)
        state = storage.get(State, state_id)  # get state object
        if state is None:
            abort(404)

        return jsonify(state.to_dict())

    if request.method == 'DELETE':
        if state_id is None:
            abort(404)
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        storage.delete(state)

        return jsonify({}), 200

    if request.method == 'PUT':
        if request.get_json:
            kwargs = request.get_json()
        else:
            return "Not a JSON", 400

        if kwargs:
            if 'name' not in kwargs.keys():
                return 'Missing name', 400

        try:
            state = storage.get(State, state_id)
            if state is None:
                abort(404)

            for k in ("id", "created_at", "updated_at"):
                kwargs.pop(k, None)
                for k, v in kwargs.items():
                    setattr(state, k, v)
            state.save()

        except AttributeError:
            return "Not a JSON", 400

    return jsonify(state.to_dict()), 200
