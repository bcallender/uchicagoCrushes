from flask import Flask, current_app
from flask.ext.pymongo import PyMongo
from datetime import timedelta, datetime

import postService
import db_connect

app = Flask("Crushes")
mongo = db_connect.connect()

db = mongo.posts


def update_data():
	with app.app_context():
			last_updated = list(db.find().sort([('created', -1)]).limit(1))[0]['created']
			date = last_updated.strftime('%s')
			postService.update_posts(date)

update_data()

