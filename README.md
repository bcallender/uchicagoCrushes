## Super quick and dirty API for UChicago Crushes that allows searching. 

	Run python setup_db.py to create the appropriate indices and fetch the latest from uchicago crushes. Make sure your mongodb is installed and running on the default port!

	Create a python virtualenv in the directory with `virtualenv env`. Then run `source env/bin/activate` then `pip install -r req.txt` to install requirements. 

	Start the application by running python app.py!

##Endpoint is localhost:5000/api/v1/posts
	1. pagination: localhost:5000/api/v1/posts?page=1
	2. search: localhost:5000/api/v1/posts?search=Love
	3. paginated search: localhost:5000/api/v1/posts?search=Love&page=4

##Next features:
	1. ...a front end
	2. currently the text search is only active on the post message itself, next up is adding a text cursor to the comment section, as often thats where names are mentioned.
	3. update with changes in uchicago crushes. currently is one use only, need to implement updating
		* related: fix fetchposts so doesn't end in error...
	4. caching so every req doesn't hit mongo. 
	5. auto-suggest recent searches with redis?
