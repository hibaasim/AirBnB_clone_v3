#!/usr/bin/python3
"""  handles all default RESTFul API actions """

from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    '''gets all amenities'''
    amenities = storage.all(Amenity).values()
    amenity_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    '''gets amenity according to id'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_amenity(amenity_id):
    '''deletes state according to id'''
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    ''' creates a new state'''
    data = request.get_json()
    if not data or request.content_type != 'application/json':
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    else:
        new_amenity = Amenity(**data)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    ''' updates an existing amenity'''
    ignore = ['id', 'created_at', 'updated_at']

    if request.content_type != 'application/json':
        abort(400, description="Not a JSON")
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        new_info = request.get_json()
        if not new_info:
            abort(400, description="Not a JSON")

        for key, value in new_info.items():
            if key not in ignore:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)
