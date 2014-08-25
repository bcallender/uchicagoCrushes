from flask import Flask, current_app
from flask.ext.pymongo import PyMongo
from datetime import timedelta, datetime

from postService import PostService
import db_connect

app = Flask("Crushes")
mongo, crushes = db_connect.connect()

db = crushes.posts


def update_data():
	with app.app_context():
			last_updated = list(db.find().sort([('created', -1)]).limit(1))[0]['created']
			date = last_updated.strftime('%s')
			ps = PostService()
			ps.updatePosts(date)

update_data()

