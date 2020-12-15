import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()

from database.models import setup_db, db_drop_and_create_all



app = Flask(__name__)
setup_db(app)
CORS(app)

#db_drop_and_create_all()

# Routes
@app.route('/')
@app.route('/login-result')
def home():
    return jsonify({
        "application name" : "Casting Agency APIs",
        "owner": "Shaker Hussien"
    })

from routes.actor import *
from routes.movie import *

# Error Handlers
from error_handlers import *

if __name__ =="__main__":
    app.run(debug=True)
