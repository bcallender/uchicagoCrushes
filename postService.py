import facebook
import requests
from flask import Flask, jsonify, abort, make_response, request, url_for, current_app

from flask.ext.pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import timedelta, datetime
from time import sleep
import random as rand
import db_connect
import os

class Post(object):
		"""docstring for Post"""
		def __init__(self, data):
			super(Post, self).__init__()
			try:
				self.message = data['message']
				self.created = datetime.strptime(data['created_time'].partition('+')[0], '%Y-%m-%dT%X')
				self.fb_id = data['id']
				self.comments = data['comments']
				self.likes = data['likes']
			except KeyError:
				pass

class PostService(object):
	"""docstring for PostService"""
	def __init__(self, test=False):
		super(PostService, self).__init__()
		self.app = Flask("Crushes")
		self.mongo, self.crushes = db_connect.connect()
		self.db = self.crushes.posts
		self.CLIENT_ID =  "686893277993623" if test else os.environ.get('fb_client_id')
		self.CLIENT_SECRET = "518865db69daa46de95171f00a56fc25" if test else os.environ.get('fb_client_secret')

	

	def authenticate(self):
		return facebook.get_app_access_token(self.CLIENT_ID, self.CLIENT_SECRET)


	def getPosts(self, **kwargs):
		oauth_token = self.authenticate()
		graph = facebook.GraphAPI(oauth_token)
		posts = graph.get_connections("UChicagoCrushes", "posts", **kwargs)
		posts_data = posts['data']
		
		processed_posts = []
		for p in posts_data:
			pst = Post(p)
			try:
				pst.message
				processed_posts.append(pst)
			except Exception, e:
				pass
		try: 
			paging_data = posts['paging']
			return processed_posts, paging_data
		except KeyError, e:
			print "Fetching Complete"
			return processed_posts, False
		

	def pgNext(self, paging):
		try:
			nxt = paging['next']
			until = nxt.partition("&until=")
			return until[2]

		except Exception, e:
			return False

	def pgPrev(self, paging):
		try:
			nxt = paging['previous']
			since = nxt.partition("&since=")
			since = since[2].partition("&")
			return since[0]

		except Exception, e:
			return False


	def getPostsSince(self, time): 
		posts, paging = self.getPosts(limit=250, since=time)
		sin = self.pgPrev(paging)
		return posts, sin

	def getPostsUntil(self, time):
		posts, paging = self.getPosts(limit=250, until=time)
		unt = self.pgNext(paging)
		return posts, unt

	def updatePosts(self, time):
		with app.app_context():
			posts, sin = self.getPostsSince(time)
			if posts:
				self.db.insert(map(lambda x: vars(x),posts))
				cond = True
				while cond:
					sleep(rand.random())
					posts, sin = self.getPostsSince(sin)
					if sin and posts:
						self.db.insert(map(lambda x: vars(x),posts))
					else: 
						cond = False

	def curatePosts(self):
		with app.app_context():
			posts, unt = self.getPostsUntil(time)
			if posts:
				self.db.insert(map(lambda x: vars(x),posts))
				cond = True
				while cond:
					sleep(rand.random())
					posts, unt = self.getPostsUntil(unt)
					if unt and posts:
						self.db.insert(map(lambda x: vars(x),posts))
					else: 
						cond = False

