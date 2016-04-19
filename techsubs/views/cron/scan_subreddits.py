import flask
from google.appengine.api import taskqueue

from techsubs import app


@app.route('/_cron/scan-subreddits')
def scan_subreddits():
    """
    Initiates a full scan of the sub-Reddits.
    """
    worker_url = flask.url_for('sr-scanner-enqueue-all')
    taskqueue.add(url=worker_url)
    return "OK"
