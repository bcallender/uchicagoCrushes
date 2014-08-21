from flask import Flask, current_app
from flask.ext.pymongo import PyMongo
import fetchPosts

app = Flask("Crushes")
mongo = PyMongo(app)


def setupIndexes():
	with app.app_context():
		mongo.db.posts.ensure_index([("message", 'text' )], name="TextIndex")
		mongo.db.posts.ensure_index([("created", -1), ("created", 1)])

setupIndexes()
fetchPosts.curate_posts()
