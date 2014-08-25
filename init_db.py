from postService import PostService()
import argparse 

parser = argparse.ArgumentParser(description="Initialize Database")
parser.add_argument('--local', help="create databse locally")
parser.parse_args()

if args['--local']:
	ps = PostService(True)
else:
	ps = PostService()

ps.curate_posts()