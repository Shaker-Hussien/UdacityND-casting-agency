from flask import Flask, request, jsonify, abort
from database.models import Actor
from auth.auth import requires_auth
from api import app


@app.route('/actors')
@requires_auth('get:actors')
def get_actors(token):
    try:
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in Actor.query.all()],
        }), 200

    except Exception as error:
        print(error)
        abort(422)


@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def add_actor(token):
    data = request.get_json()
    actor_name = data.get('name', None)
    actor_age = data.get('age', None)
    actor_gender = data.get('gender', None)

    if not actor_name or not actor_age or not actor_gender:
        abort(400)

    existing_actor = Actor.query.filter(
        Actor.name == actor_name,
        Actor.age == actor_age,
        Actor.gender == actor_gender).one_or_none()

    if existing_actor:
        abort(422)

    try:
        actor_data = Actor(name=actor_name, age=actor_age, gender=actor_gender)
        actor_data.insert()

        return jsonify({
            'success': True,
            'actor': actor_data.format()
        }), 201

    except Exception as error:
        print(error)
        abort(422)


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def edit_actor(token, actor_id):
    actor_data = Actor.query.get(actor_id)

    if not actor_data:
        abort(404)

    data = request.get_json()
    updated_name = data.get('name', None)
    updated_age = data.get('age', None)
    updated_gender = data.get('gender', None)

    try:

        if updated_name and actor_data.name != updated_name:
            actor_data.name = updated_name

        if updated_age and actor_data.age != updated_age:
            actor_data.age = updated_age

        if updated_gender and actor_data.gender != updated_gender:
            actor_data.gender = updated_gender

        actor_data.update()

        return jsonify({
            'success': True,
            'actor': actor_data.format()
        }), 200

    except Exception as error:
        print(error)
        abort(422)


@ app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(token, actor_id):
    actor_data = Actor.query.get(actor_id)
    if not actor_data:
        abort(404)

    try:
        actor_data.delete()
        return jsonify({
            "success": True,
            "deleted": actor_data.id
        }), 200
    except Exception as error:
        print(error)
        abort(422)
