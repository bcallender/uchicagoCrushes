Super quick and dirty API for UChicago Crushes that allows searching. 

Run python setup_db.py to create the appropriate indices and fetch the latest from uchicago crushes. Make sure your mongodb is installed and running on the default port!

Create a python virtualenv in the directory with 'virtualenv env'. Then run 'source env/bin/activate' then 'pip install -r req.txt' to install requirements. 

Endpoint is localhost:5000/api/v1/posts
	pagination: localhost:5000/api/v1/posts?page=1
	search: localhost:5000/api/v1/posts?search=Love
	paginated search: localhost:5000/api/v1/posts?search=Love&page=4

Next features:
	-...a front end
	-currently the text search is only active on the post message itself, next up is adding a text cursor to the comment section, as often thats where names are mentioned.
	-update with changes in uchicago crushes. currently is one use only, need to implement updating
		-related: fix fetchposts so doesn't end in error...
	-caching so every req doesn't hit mongo. 
	-auto-suggest recent searches with redis?
