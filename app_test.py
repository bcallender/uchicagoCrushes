import os
import app
import unittest
import db_connect
from flask import Flask, current_app
from flask.ext.pymongo import PyMongo

class app(unittest.TestCase):

    def setUp(self):
		self.app = Flask("Crushes")
		self.mongo = db_connect.connect()
		self.db = self.mongo.posts

    def test_db_connection(self):
    	with self.app.app_context(): 
    		self.assertEqual(len(list(self.db.find().limit(25))), 25)


if __name__ == '__main__':
    unittest.main()