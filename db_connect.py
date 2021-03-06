from flask.ext.pymongo import PyMongo, MongoClient
import os
from urlparse import urlparse


def connect():
	MONGO_URL = os.environ.get('MONGOLAB_URI')
	 
	if MONGO_URL:
	  # Get the database
	  mongo = MongoClient(MONGO_URL)
	  crushes = mongo[MONGO_URL.rpartition('/')[2]]
	else:
	  # Not on an app with the MongoHQ add-on, do some localhost action
	  mongo = MongoClient()
	  crushes = mongo.Crushes
	return mongo, crushes

