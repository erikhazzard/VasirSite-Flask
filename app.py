# ==============================================================================
# app.py
#   A backend example for the proto demo.  Will serve up data and static pages
#
# ==============================================================================
import flask
import pymongo 
import datetime
import json
import re
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
    return flask.render_template('home.html')

@app.route('/about/')
def about():
    return flask.render_template('about.html')

@app.route('/dev/')
def dev():
    return flask.render_template('dev.html')

@app.route('/openlayers_book/')
def book():
    return flask.render_template('openlayers_book.html')

@app.route('/blog/')
def blog():
    return flask.render_template('blog.html')
# ==============================================================================
#
# Posts
#
# ==============================================================================
@app.route('/items/')
@app.route('/items/<query>/')
def items(query=None):
    '''Gets items from mongo based on query
    '''
    #Get the items from the database based on the query (if any)
    db_items = get_items_from_query(query)

    items = [] 
    for item in db_items:
        #Remove the _id since it's returned as an ObjectID object
        del(item['_id'])
        items.append(item)

    #Get the total length
    num_results = len(items)
    
    res = {
        "models": items, 
        "num_results": num_results
    }
    return flask.jsonify(res)

# ==============================================================================
#
# Run server
#
# ==============================================================================
if __name__ == "__main__":
    if ENV == 'develop':
        app.debug = True
    app.run(port=PORT)
