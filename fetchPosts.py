import facebook
import requests
from flask import Flask, jsonify, abort, make_response, request, url_for, current_app

from flask.ext.pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import timedelta, datetime
from time import sleep
import random as rand

import fetchPosts

app = Flask("Crushes")
mongo = PyMongo(app)


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


def getPosts(**kwargs):
	print 'fetching posts'
	oauth_token = facebook.get_app_access_token('686893277993623', '518865db69daa46de95171f00a56fc25')
	graph = facebook.GraphAPI(oauth_token)
	posts = graph.get_connections("UChicagoCrushes", "posts", **kwargs)
	posts_data = posts['data']
	try: 
		paging_data = posts['paging']
	except KeyError, e:
		raise StandardError("Parsing Complete")
	processed_posts = []
	print 'processing posts'
	for p in posts_data:
		pst = Post(p)
		try:
			pst.message
			processed_posts.append(pst)
		except Exception, e:
			pass
			
	return processed_posts, paging_data

def parse_paging(paging):
	try:
		nxt = paging['next']
		until = nxt.partition("&until=")
		return until[2]
	except KeyError, e:
		return False


def curate_posts():
	with app.app_context():
		def proc(post):
			return vars(post)

		posts, paging = getPosts(limit=250)
		unt = parse_paging(paging)
		mongo.db.posts.insert(map(proc,posts))
		cond = True
		while cond:
			sleep(rand.random())
			posts, paging = getPosts(limit=250, until=unt)
			unt = parse_paging(paging)
			if unt:
				mongo.db.posts.insert(map(proc,posts))
			else: 
				mongo.db.posts.insert(map(proc,posts))
				cond = False

curate_posts()