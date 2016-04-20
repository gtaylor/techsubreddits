import flask
from google.appengine.api import taskqueue

from techsubs import app
from techsubs import subreddits
from techsubs.bucket_populator import category_overview


@app.route('/_workers/static-gen/category/overview/enqueue-all',
           endpoint='json-category-overview-enqueue-all')
def enqueue_all_overview_json_population():
    """
    Initiates a full generation and upload of all Subreddit category
    index overview JSON documents.
    """
    for category in subreddits.CATEGORIES.keys():
        gen_worker = flask.url_for(
            'json-category-overview-json', category=category)
        taskqueue.add(url=gen_worker, queue_name='bucket-populator-workers')
    return "OK"


@app.route('/_workers/static-gen/category/<category>/overview/json',
           endpoint='json-category-overview-json', methods=['POST'])
def gen_and_upload_category_overview_json(category):
    """
    Generates and uploads a Subreddit category's overview JSON.
    """
    category_overview.generate_and_upload(category)
    return "OK"
