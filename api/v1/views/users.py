#!/usr/bin/python3
"""  handles all default RESTFul API actions """

from flask import jsonify, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    '''gets all users'''
    users = storage.all(User).values()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)


@app_views.route('users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    '''gets user according to id'''
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    '''deletes user according to id'''
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    ''' creates a new user'''
    data = request.get_json()
    if not data or request.content_type != 'application/json':
        abort(400, description="Not a JSON")
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    new_user = user(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    ''' updates an existing user'''
    ignore = ['id', 'email', 'created_at', 'updated_at']

    if request.content_type != 'application/json':
        abort(400, description="Not a JSON")
    user = storage.get(User, user_id)
    if user:
        new_info = request.get_json()
        if not new_info:
            abort(400, description="Not a JSON")

        for key, value in new_info.items():
            if key not in ignore:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        abort(404)
