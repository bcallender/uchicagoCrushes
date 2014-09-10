#!flask/bin/python
import facebook
import requests
from flask import Flask, jsonify, abort, make_response, request, url_for, g, render_template
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from datetime import timedelta, datetime
from flask import current_app
from functools import update_wrapper
from time import sleep
import random as rand
import db_connect

app = Flask("Crushes")

def output_json(obj, code, headers=None):
    """
    This is needed because we need to use a custom JSON converter
    that knows how to translate MongoDB types to JSON.
    """
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp
#CORS setup
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        f.required_methods = ['OPTIONS']
        return update_wrapper(wrapped_function, f)
    return decorator





@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.before_request
def before_request():
	mongo = getattr(g, 'mongo', None)
	db = getattr(g, 'db', None)
	if mongo is None or db is None:
		g.mongo, g.crushes = db_connect.connect()
		g.db = g.crushes.posts

@app.teardown_request
def teardown_request(exception):
	mongo = getattr(g, 'mongo', None)


api = Api(app)
api.decorators = [crossdomain(origin='*', methods= ['GET',], headers=['accept', 'Content-Type'])]
DEFAULT_REPRESENTATIONS = {'application/json': output_json}
api.representations = DEFAULT_REPRESENTATIONS


def marshalPosts(posts, res, pg):
	return [{'posts':posts}, {'total_results': res}, {'page': pg}]

def createSearchQuery(search):
	return {'$text': {'$search': "\"" + search + "\""}}


class PostsListAPI(Resource):
	#decorators = [auth.login_required]
	def __init__(self):
		self.parser = reqparse.RequestParser()
		self.parser.add_argument('page', type=int)
		self.parser.add_argument('search', type=str)
		super(PostsListAPI, self).__init__()
	def get(self):
		args = self.parser.parse_args()
		if args['page'] and args['search']:
			page = args['page']
			search = createSearchQuery(args['search'])
			cursor = g.db.find(search)
			rescount = cursor.count()
			posts = list(cursor.limit(25).skip((page - 1)*25).sort([('created', -1)]))
			return marshalPosts(posts, rescount, page)
		if args['page']:
			page = args['page']
			rescount = g.db.find().count()
			posts = list(g.db.find().limit(25).skip((page - 1)*25).sort([('created', -1)]))
			return marshalPosts(posts, rescount, page)
		elif args['search']:
			search = createSearchQuery(args['search'])
			cursor = g.db.find(search)
			rescount = g.db.find(search).count()
			posts = list(cursor.limit(25).sort([('created',-1)]))
			return marshalPosts(posts, rescount, 1)
		else:
			rescount = g.db.find().count()
			posts = list(g.db.find().limit(25).sort([('created',-1)]))
			return marshalPosts(posts, rescount, 1)





class PostAPI(Resource) :

 	def __init__(self):
		super(PostAPI, self).__init__()
	def get(self, id):
		post = db.find_one({"_id": ObjectId(id)})
		if not post :
			abort(404)
		return { 'post' : post}

api.add_resource(PostsListAPI, '/api/v1/posts', endpoint = 'posts')
api.add_resource(PostAPI, '/api/v1/posts/<id>', endpoint = 'post')





if __name__ == '__main__':
    app.run(debug = True)
