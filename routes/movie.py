from flask import Flask, request, jsonify, abort
from database.models import Movie

from auth.auth import AuthError, requires_auth
from api import app


@app.route('/movies')
@requires_auth('get:movies')
def get_movies(token):
    try:
        return jsonify({
            'success': True,
            'movies': [actor.format() for actor in Movie.query.all()],
        }), 200
    except Exception as error:
        print(error)
        abort(422)


@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def add_movie(token):
    data = request.get_json()
    movie_title = data.get('title', None)
    movie_release_date = data.get('release_date', None)

    if not movie_title or not movie_release_date:
        abort(400)

    existing_movie = Movie.query.filter(
        Movie.title == movie_title,
        Movie.release_date == movie_release_date).one_or_none()

    if existing_movie:
        abort(422)

    try:
        movie_data = Movie(title=movie_title, release_date=movie_release_date)
        movie_data.insert()

        return jsonify({
            'success': True,
            'movie': movie_data.format()
        }), 201

    except Exception as error:
        print(error)
        abort(422)


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def edit_movie(token, movie_id):
    movie_data = Movie.query.get(movie_id)

    if not movie_data:
        abort(404)

    data = request.get_json()
    updated_title = data.get('title', None)
    updated_release_date = data.get('release_date', None)

    try:

        if updated_title and movie_data.title != updated_title:
            movie_data.title = updated_title

        if updated_release_date and \
                movie_data.release_date != updated_release_date:
            movie_data.release_date = updated_release_date

        movie_data.update()

        return jsonify({
            'success': True,
            'movie': movie_data.format()
        }), 200

    except Exception as error:
        print(error)
        abort(422)


@ app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(token, movie_id):
    movie_data = Movie.query.get(movie_id)
    if not movie_data:
        abort(404)

    try:
        movie_data.delete()
        return jsonify({
            "success": True,
            "deleted": movie_data.id
        }), 200
    except Exception as error:
        print(error)
        abort(422)
