import os
import app
import unittest
import db_connect
from postService import PostService
from datetime import timedelta, datetime, date
from flask import Flask, current_app
from flask.ext.pymongo import PyMongo

class app(unittest.TestCase):

    def setUp(self):
    	self.app = Flask("Crushes")
    	self.mongo, self.db = db_connect.connect()
    	self.db = self.db.posts
    	self.ps = PostService(True)

    def testDBConnection(self):
    	with self.app.app_context(): 
    		self.assertEqual(len(list(self.db.find().limit(25))), 25)

    def testFBAuthentication(self):
    	oauth_token = self.ps.authenticate()
    	self.assertTrue(oauth_token is not None)

    def testFBFetch(self):
    	processedPosts, paging = self.ps.getPosts(limit=5)
    	self.assertTrue("UChicago" in processedPosts[0].message )
    	self.assertTrue(paging['next'] is not None)
    	self.assertTrue(paging['previous'] is not None)

	def testFBUpdateYesterday(self):
		yesterday = datetime.now() - timedelta(days=1)
		posts, paging = self.ps.getPostsSince(yesterday.strftime("%s"))
		self.assertTrue(paging is not False)
		self.assertTrue(len(posts) > 0)

    def testFBUpdateNow(self):
    	posts, paging = self.ps.getPostsSince(datetime.now().strftime("%s"))
    	self.assertTrue(paging is False)
    	self.assertTrue(len(posts) == 0)
		
	

   	def tearDown(self):
   		self.mongo.disconnect()


if __name__ == '__main__':
    unittest.main()