import flask
from google.appengine.api import taskqueue

from techsubs import app
from techsubs.bucket_populator import category_overview


@app.route('/_cron/scan-subreddits')
def scan_subreddits():
    """
    Initiates a full scan of the sub-Reddits.
    """
    worker_url = flask.url_for('sr-scanner-enqueue-all')
    taskqueue.add(url=worker_url, queue_name='subreddit-api-workers')
    return "OK"


@app.route('/_cron/gen-and-upload-api-json')
def subreddit_category_overview(subreddit_category):
    category_overview.generate_and_upload(subreddit_category)
    return 'OK'
