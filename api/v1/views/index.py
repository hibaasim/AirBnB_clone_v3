#!/usr/bin/python3
"""routing"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """routes a specific message for status"""
    return jsonify({"status": "OK"})
