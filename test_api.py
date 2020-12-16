
from database.models import setup_db, Actor, Movie
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from api import app


class AgencyTestCase(unittest.TestCase):
    """This class represents the casting agency project test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        setup_db(self.app)

        self.producer_token = {
            "Authorization": f"Bearer {os.getenv('producer_token')}"
        }
        self.director_token = {
            "Authorization": f"Bearer {os.getenv('director_token')}"
        }
        self.assistant_token = {
            "Authorization": f"Bearer {os.getenv('assistant_token')}"
        }

        self.new_actor = {
            "name": "new_actor",
            "age": 30,
            "gender": "Male"
        }

        self.new_movie = {
            "title": "new_movie",
            "release_date": '10-12-2020'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            # create all tables
            # self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['actors'], None)

    def test_add_actor(self):
        res = self.client().post('/actors',
                                 headers=self.producer_token,
                                 json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['actor'], None)

    def test_add_actor_duplicate(self):
        res = self.client().post('/actors',
                                 headers=self.producer_token,
                                 json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_edit_actor(self):
        res = self.client().patch('/actors/1',
                                  headers=self.producer_token, json={
                                      "name": "actor_01_edited"
                                  })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['actor'], None)

    def test_edit_actor_not_exist(self):
        res = self.client().patch('/actors/1000',
                                  headers=self.producer_token,
                                  json={
                                      "name": "new_actor_edited"
                                  })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_actor(self):
        res = self.client().delete('/actors/5', headers=self.producer_token)
        data = json.loads(res.data)
        actor_data = Actor.query.filter(Actor.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)
        self.assertEqual(actor_data, None)

    def test_delete_actor_not_exist(self):
        # id for not existing actor
        res = self.client().delete('/actors/1000', headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['movies'], None)

    def test_add_movie(self):
        res = self.client().post('/movies',
                                 headers=self.producer_token,
                                 json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['movie'], None)

    def test_add_movies_duplicate(self):
        res = self.client().post('/movies',
                                 headers=self.producer_token,
                                 json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_edit_movie(self):
        res = self.client().patch('/movies/1',
                                  headers=self.producer_token,
                                  json={
                                      "title": "movie_01_edited"
                                  })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['movie'], None)

    def test_edit_movie_not_exist(self):
        res = self.client().patch('/movies/1000',
                                  headers=self.producer_token,
                                  json={
                                      "title": "edited_title"
                                  })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movie(self):
        res = self.client().delete('/movies/5', headers=self.producer_token)
        data = json.loads(res.data)
        movie_data = Movie.query.filter(Movie.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 5)
        self.assertEqual(movie_data, None)

    def test_delete_movie_not_exist(self):
        # id for not existing movie
        res = self.client().delete('/movies/1000', headers=self.producer_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_allow_permision_assistant(self):
        res = self.client().get('/actors', headers=self.assistant_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_deny_permision_assistant(self):
        res = self.client().post('/actors',
                                 headers=self.assistant_token,
                                 json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_allow_permision_director(self):
        res = self.client().get('/movies', headers=self.director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_deny_permision_director(self):
        res = self.client().delete('/movies/1', headers=self.director_token)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
