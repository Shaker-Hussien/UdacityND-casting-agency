import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from database.models import setup_db, db_drop_and_create_all


app = Flask(__name__)
setup_db(app)
CORS(app)


# Routes
@app.route('/')
def home():
    return jsonify({
        "application name": "Casting Agency APIs",
        "owner": "Shaker Hussien"
    })


from routes.actor import *  # noqa: E402
from routes.movie import *  # noqa: E402

# Error Handlers
from error_handlers import *  # noqa: E402

if __name__ == "__main__":
    app.run(debug=True)
