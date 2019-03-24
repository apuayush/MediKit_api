# Tornado libraries
from tornado.web import RequestHandler, Application, removeslash
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import parse_command_line
from tornado.gen import coroutine

import json
import os
import requests
import jwt
import time
import uuid
import base64
from datetime import datetime
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
# import env

try:
    import controllers.secrets.env as env

    JWT_SECRET = env.JWT_SECRET
    JWT_ALGORITHM = env.JWT_ALGORITHM
except:
    JWT_SECRET = os.environ['JWT_SECRET']
    JWT_ALGORITHM = os.environ['JWT_ALGORITHM']

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials
cred = credentials.Certificate("controllers/secrets/firebase_secret.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
