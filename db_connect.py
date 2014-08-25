from flask.ext.pymongo import PyMongo, MongoClient
import os
from urlparse import urlparse


def connect():
	MONGO_URL = os.environ.get('MONGOHQ_URL')
	 
	if MONGO_URL:
	  # Get the database
	  mongo = MongoClient(MONGO_URL)
	else:
	  # Not on an app with the MongoHQ add-on, do some localhost action
	  mongo = MongoClient()

	return mongo

