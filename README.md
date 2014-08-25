
## Super quick and dirty API for UChicago Crushes that allows searching. 

Create a python virtualenv in the directory with `virtualenv env`. Then run `source env/bin/activate` then `pip install -r requirements.txt` to install requirements. 

Run `python setup_db.py`, then `python init_db.py` to create the appropriate indices and fetch the latest from uchicago crushes. Make sure your mongodb is installed and running on the default port!

Start the application by running foreman start (or python app.py if you dont have foreman)!

Or just go to http://murmuring-oasis-3072.herokuapp.com/api/v1/posts

## Are there tests?

...a couple. well, one.

`python app_test.py`

##Endpoint is localhost:5000/api/v1/posts
	1. pagination: localhost:5000/api/v1/posts?page=1
	2. search: localhost:5000/api/v1/posts?search=Love
	3. paginated search: localhost:5000/api/v1/posts?search=Love&page=4

##Next features:
	0. tests
	1. ...a front end
	2. currently the text search is only active on the post message itself, next up is adding 
	a text cursor to the comment section, as often thats where names are mentioned.
	4. caching so every req doesn't hit mongo. 
	5. auto-suggest recent searches with redis?
	6. single post API with live fetching of likes and comments from fb
	7. support for the existing hashtag system/linking to old posts based on uchicago crush id, or hashtag
	8. fb login and interaction (commenting, liking)
	9. scoring system
