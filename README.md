# Casting Agency Backend APIs

### Introduction

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

### Motivation

The Casting Agency Project will allow me to apply many concepts and techniques essential for any **Full-Stack Enginner** like:

- Applying Database Modeling and Migration concepts.
- Applying REST APIs principles.
- Applying Authentication/Authorization and Users/Roles Concepts.
- Applying Cloud Deployment on Heroku.
- using Postman for documentation and testing.

## Getting Started

### Tech Stack

Our tech stack will include:

- **SQLAlchemy ORM** to be our ORM library of choice
- **PostgreSQL** as our database of choice
- **Python3** and **Flask** as our server language and server framework
- **Flask-Migrate** for creating and running schema migrations

### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic and [Flask-Script](https://flask-script.readthedocs.io/en/latest/) provides support for writing external scripts in Flask

### Main Files: Project Structure

```
├── README.md
├── requirements.txt *** The dependencies we need to install
├── api.py *** the main driver of the app.
├── test_api.py *** unit tests for the apis.
├── Procfile ***  for Heroku deployment
├── manage.py *** used to run migration
├── error_handlers.py *** the error handlers implemented for the apis (400,404,405,422,AuthError)
│
├── routes
│   ├── actor  *** routes related to actor apis
│   └── movie  *** routes related to movie apis
│
├── database
│   └── models *** contains the models used Actor,Movie and helper function to setup connection with db.
│
├── auth
│   └── auth *** Authenticating the user and getting permission allowed
│
└── migrations *** migration folder to track changes in db models

```

## Development Setup

### Python

- Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

### Virtual Enviornment

- Create virtual environment for clean Setup

```
 > cd YOUR_PROJECT_DIRECTORY_PATH/
 > virtualenv venv
 > .\venv\Scripts\activate
```

### PIP Dependencies

Once you have your virtual environment install all needed dependencies by running:

```
> pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

### Create the database

- Create postgres DB named casting_agency [for development]/ casting_agency_test [for testing] from psql shell or using GUI

  ```
  > createdb casting_agency
  > createdb casting_agency_test
  ```

- For Development : Edit DATABASE_URL in .env file. Replace database-user & password with yours & TEST= False.
- For Testing : Edit TEST_DATABASE_URL in .env file. Replace database-user & password with yours & TEST= True.

### Apply Migration to the database

- Apply migration provided to populate the Schema with test data.
- I already added static data insert queries and executed them in upgrade function.\
  [for running unit test make sure you already applied migration to testing database TEST=True in .env]

```
  > python manage.py db upgrade
```

### Run the development server:

```
> SET FLASK_APP=api
> SET FLASK_ENV=development
> flask run
```

### Run the unit tests:

```
> python test_api.py
```

### Heroku Deployment

- [Link](https://casting-agency-shaker.herokuapp.com/)

### Authentication Info

- Name : CastingAgency
- Domain : dev-shaker.auth0.com
- Login : [link](https://dev-shaker.auth0.com/authorize?audience=agency&response_type=token&client_id=77FxF5HjVct5MB14659YeW58NlmuE56t&redirect_uri=https://casting-agency-shaker.herokuapp.com/)

- Users & Roles

  - Casting Assistant

    - mail: assistant_user@mail.com , pass: assistantpass_123
    - Permissions:
      - Can view actors and movies

  - Casting Director
    - mail: director_user@mail.com , pass: directorpass_123
    - Permissions:
      - All permissions a Casting Assistant has and…
      - Add or delete an actor from the database
      - Modify actors or movies
  - Executive Producer
    - mail: producer_user@mail.com , pass: producerpass_123
    - Permissions:
      - All permissions a Casting Director has and…
      - Add or delete a movie from the database

### Endpoints Info

GET /actors

- return all actors

```json
{
  "actors": [
    {
      "age": <actor_age>,
      "gender": "<actor_gender",
      "name": "<actor_name>"
    },
    etc...
  ],
  "success": true
}
```

POST /actors

- add new actor to the database

It receives a new actor data to be added in JSON format that looks like this:

```json
{
  "name": "<actor_name>",
  "age": <actor_age>,
  "gender": "<actor_gender>"
}
```

It should return response that looks like this:

```json
{
    "actor": {
      "name": "<actor_name>",
      "age": <actor_age>,
      "gender": "<actor_gender>"
    },
    "success": true
}
```

PATCH /actors/<actor_id>

- edit actor data

It receives actor data needed to be edited in JSON format that looks like this:

```json
{
  "name": "<new_name>"
}
```

It should return response that looks like this:

```json
{
    "actor": {
      "name": "<new_name>",
      "age": <actor_age>,
      "gender": "<actor_gender>"
    },
    "success": true
}
```

DELETE /actors/<actor_id>

- delete actor from the database

```json
{
    "deleted": <actor_id>,
    "success": true
}
```

GET /movies

- return all movies

```json
{
  "movies": [
    {
      "release_date": "<release_date>",
      "title": "<movie_title>"
    },
    etc...
  ],
  "success": true
}
```

POST /movies

- add new movie to the database

It receives a new movie data to be added in JSON format that looks like this:

```json
{
  "title": "<movie_title>",
  "release_date": "<movie_release_date>"
}
```

It should return response that looks like this:

```json
{
  "movie": {
    "title": "<movie_title>",
    "release_date": "<movie_release_date>"
  },
  "success": true
}
```

PATCH /movies/<movie_id>

- edit movie data

It receives movie data needed to be edited in JSON format that looks like this:

```json
{
  "title": "<new_title>"
}
```

It should return response that looks like this:

```json
{
  "movie": {
    "title": "<new_title>",
    "release_date": "<movie_release_date>"
  },
  "success": true
}
```

DELETE /movies/<movie_id>

- delete movie from the database

```json
{
    "deleted": <movie_id>,
    "success": true
}
```
