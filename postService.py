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

app = Flask("Crushes")
mongo = db_connect.connect()
db = mongo.posts


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
	
	processed_posts = []
	print 'processing posts'
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
	

def pg_next(paging):
	try:
		nxt = paging['next']
		until = nxt.partition("&until=")
		return until[2]

	except Exception, e:
		return False

def pg_prev(paging):
	try:
		nxt = paging['previous']
		since = nxt.partition("&since=")
		since = since[2].partition("&")
		return since[0]

	except Exception, e:
		return False

def update_posts(time): 
	with app.app_context():
		def proc(post):
			return vars(post)

		posts, paging = getPosts(limit=250, since=time)
		unt = pg_prev(paging)
		if posts:
			db.insert(map(proc,posts))
			cond = True
			while cond:
				sleep(rand.random())
				posts, paging = getPosts(limit=250, since=unt)
				unt = pg_prev(paging)
				if unt and posts:
					db.insert(map(proc,posts))
				else: 
					cond = False


def curate_posts():
	with app.app_context():
		def proc(post):
			return vars(post)

		posts, paging = getPosts(limit=250)
		unt = pg_next(paging)
		db.insert(map(proc,posts))
		cond = True
		while cond:
			sleep(rand.random())
			posts, paging = getPosts(limit=250, until=unt)
			unt = pg_next(paging)
			if unt and posts:
				db.insert(map(proc,posts))
			else: 
				cond = False
