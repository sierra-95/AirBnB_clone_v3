#!/usr/bin/python3
""" Users RESTful API """

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.base_model import BaseModel
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """ Retrieves all User objects """
    all_users = storage.all("User")
    list = []
    for user in all_users.values():
        list.append(user.to_dict())
    return jsonify(list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user(user_id):
    """ Retrieves a User object, or returns a 404 if
    the user_id is not linked to any object """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a User object, or returns a 404 if the user_id is not
    linked to any object """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a User object, or returns a 400 if the HTTP body request is not
    valid JSON, or if the dict doesn't contain the key name """
    data = ""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    email = data.get("email")
    pwd = data.get("password")
    if email is None:
        abort(400, "Missing email")
    if pwd is None:
        abort(400, "Missing password")

    new_user = User()
    new_user.first_name = data.get("first_name")
    new_user.last_name = data.get("last_name")
    new_user.email = email
    new_user.password = pwd
    new_user.save()
    return (jsonify(new_user.to_dict())), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a User object, or returns a 400 if the HTTP body is not valid
    JSON, or a 404 if user_id is not linked to an object """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    data = ""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    for k, v in data.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
    user.save()
    return (jsonify(user.to_dict()))
