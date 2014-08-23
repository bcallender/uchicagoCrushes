import facebook
import requests
from flask import Flask, jsonify, abort, make_response, request, url_for, current_app

from flask.ext.pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import timedelta, datetime
from time import sleep
import random as rand
import postService
from dateutil import parser 

app = Flask("Crushes")
mongo = PyMongo(app)

def update_data():
	with app.app_context():
			last_updated = list(mongo.db.posts.find().sort([('created', -1)]).limit(1))[0]['created']
			date = last_updated.strftime('%s')
			postService.update_posts(date)
