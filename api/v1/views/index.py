#!/usr/bin/python3
"""routing"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """routes a specific message for status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def get_stats():
    """counts the number of objects by type"""
    stats = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }
    return jsonify(stats)
