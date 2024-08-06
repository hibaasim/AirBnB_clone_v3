#!/usr/bin/python3
"""  handles all default RESTFul API actions """

from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all():
    '''gets all states'''
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_id(state_id):
    '''gets state according to id'''
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_id(state_id):
    '''deletes state according to id'''
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    ''' creates a new state'''
    state = request.get_json()
    if not state or request.content_type != 'application/json':
        abort(400, description="Not a JSON")
    if 'name' not in state:
        abort(400, description="Missing name")
    else:
        new_state = State(**state)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    ''' updates an existing state'''
    ignore = ['id', 'created_at', 'updated_at']

    if request.content_type != 'application/json':
        abort(400, description="Not a JSON")
    state = storage.get(State, state_id)
    if state:
        new_info = request.get_json()
        if not new_info:
            abort(400, description="Not a JSON")

        for key, value in new_info.items():
            if key not in ignore:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        abort(404)
