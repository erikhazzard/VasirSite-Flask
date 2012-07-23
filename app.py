# ==============================================================================
# app.py
#   A backend example for the proto demo.  Will serve up data and static pages
#
# ==============================================================================
import flask
import pymongo 
import redis
import json
from backend import settings

# ==============================================================================
#
# Setup flask app
#
# ==============================================================================
app = flask.Flask(__name__)
DB_CONNECTION = pymongo.Connection('localhost', 27017)
DB = DB_CONNECTION.vasir_site

#Settings from config
PORT = getattr(settings, 'PORT', 8080)
ENV = getattr(settings, 'ENV', 'develop')

#Get redis connection
redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)
CACHE_PREFIX = 'vasir_site:'

# ==============================================================================
#
# Static Endpoints
#
# ==============================================================================
def render_skeleton(template_name='index.html', **kwargs):
    '''Base render func, everything get passed through here
    '''
    return flask.render_template(template_name, **kwargs)

@app.route('/')
def index():
    #Get latest posts
    ret = {}
    ret['latest_post'] = {}
    return render_skeleton('home.html', **ret)

@app.route('/about/')
def about():
    return render_skeleton('about.html')

@app.route('/dev/')
def dev():
    return render_skeleton('dev.html')

@app.route('/openlayers_book/')
def book():
    return render_skeleton('openlayers_book.html')

# ==============================================================================
# BLOG
# ==============================================================================
@app.route('/blog/')
@app.route('/blog/<category>/')
@app.route('/blog/<category>/<slug>/')
def blog(category=None, slug=None):
    '''Handles grabbing blog posts by date / category / tag 
    '''
    #Setup return object
    ret = {
        'posts': [],
        'post': False,
        'categories': {}
    }
    
    #Template name will be either blog.html (for all posts / categories)
    #   or post_single.html (for individual posts)
    template_name = 'blog.html'

    #------------------------------------
    #Get from cache
    #------------------------------------
    cache_key = CACHE_PREFIX + json.dumps({'category': category, 'slug': slug})
    cache_res = redisClient.get(cache_key)
    #If there's something in the cache, return it
    if cache_res is not None:
        cached = json.loads(cache_res) 
        return render_skeleton(cached['template_name'], **cached['ret'])

    #------------------------------------
    #Not cached, Get posts based on query
    #------------------------------------
    if category is None and slug is None:
        #All posts
        db_posts = DB.posts.find().sort('post_date', -1)

    elif category is not None and slug is None:
        #Only category posts
        db_posts = DB.posts.find({
            'category': category    
        }).sort('post_date', -1)

    elif category is not None and slug is not None:
        #Single post
        db_posts = DB.posts.find({
            'slug': slug
        }).sort('post_date', -1)

        #Render to the single post page
        template_name = 'post_single.html'

    #------------------------------------
    #Setup response
    #------------------------------------
    #For all posts, category, and tag pages
    #Posts that are shown in left side of page
    for post in db_posts:
        #Add to the posts
        #Don't use _id
        post.pop('_id')
        ret['posts'].append(post)

    #------------------------------------
    #For all pages
    #------------------------------------
    #Info about posts
    all_posts = []

    #Get ALL posts and categories
    all_posts, ret['categories'] = get_all_posts_and_categories()

    #Get latest posts, which is just the last 5 posts
    ret['latest_posts'] = all_posts[0:5]

    #If no category and slug was passed, they're asking for all posts
    ret['total_posts'] = len(all_posts)

    #------------------------------------
    #Save to cache
    #------------------------------------
    #Save to cache
    cache_dict =  {
        'template_name': template_name,
        'ret': ret
    }
    #Save to cache
    #TODO: set TTL
    redisClient.set(cache_key, json.dumps(cache_dict))

    #Return response, pass in ret object (unpack values)
    return render_skeleton(template_name, **ret)

#----------------------------------------
#Get the latest posts to show across all parts of the blog
#----------------------------------------
def get_latest_posts():
    latest_posts = blog_models.Post.objects.order_by('-post_date')[:5]
    return latest_posts

def get_all_posts_and_categories():
    '''Grabs all the posts and categories from the DB,
    using redis for cache
    '''
    #Check cache
    all_db_posts = DB.posts.find().sort('post_date', -1)

    cache_key = CACHE_PREFIX + 'all_posts_categories'
    cache_res = redisClient.get(cache_key)
    #If there's something in the cache, return it
    if cache_res is not None:
        cached = json.loads(cache_res) 
        return (cached['all_posts'], cached['categories'])

    #------------------------------------
    #Not cached, setup posts and categories
    #------------------------------------
    all_posts = []
    categories = {}
    
    #Get posts
    for post in all_db_posts:
        #Don't use _uid
        post.pop('_id')
        all_posts.append(post)

         #Keep track of categories for ALL posts
        try:
            categories[post['category']]['num'] += 1
        except KeyError:
            categories[post['category']] = {}
            #Keep track of count
            categories[post['category']]['num'] = 1
            #Get nice name to show
            categories[post['category']][
                'pretty_name'] = post['category'].replace(
                '_', ' ').capitalize()

    #------------------------------------
    #Set cache
    #------------------------------------
    cache_dict =  {
        'all_posts': all_posts,
        'categories': categories
    }
    #Write it
    redisClient.set(cache_key, json.dumps(cache_dict))

    return (all_posts, categories)

# ==============================================================================
#
# Run server
#
# ==============================================================================
if __name__ == "__main__":
    if ENV == 'develop':
        app.debug = True
    app.run(port=PORT)
