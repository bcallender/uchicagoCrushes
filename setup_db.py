from flask import Flask, current_app
from flask.ext.pymongo import PyMongo
import postService
import db_connect

app = Flask("Crushes")
mongo = db_connect.connect()
db = mongo.posts


def setupIndexes():
	with app.app_context():
		db.ensure_index([("message", 'text' )], name="TextIndex")
		db.ensure_index([("created", 1)])

setupIndexes()
postService.curate_posts()
