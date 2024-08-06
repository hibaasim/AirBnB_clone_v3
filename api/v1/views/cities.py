#!/usr/bin/python3
"""  handles all default RESTFul API actions """

from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    '''gets all cities of a state'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city_list = [city.to_dict() for city in state.cities]
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    '''gets city according to id'''
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    '''deletes city according to id'''
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city():
    ''' creates a new city'''
    new_info = request.get_json()
    if not new_info or request.content_type != 'application/json':
        abort(400, description="Not a JSON")

    if 'name' not in new_info:
        abort(400, description="Missing name")

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    new_info['state_id'] = state_id
    new_city = City(**new_info)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    ''' updates an existing city'''
    ignore = ['id', 'created_at', 'updated_at']

    if request.content_type != 'application/json':
        abort(400, description="Not a JSON")
    city = storage.get(City, city_id)
    if city:
        new_info = request.get_json()
        if not new_info:
            abort(400, description="Not a JSON")

        for key, value in new_info.items():
            if key not in ignore:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)
