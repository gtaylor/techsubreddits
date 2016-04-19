import flask
from google.appengine.api import taskqueue

from techsubs import app
from techsubs import subreddits
from techsubs.sr_scanner.scanner import full_subreddit_scan


@app.route('/_workers/sr_scanner/enqueue-all', methods=['POST'],
           endpoint='sr-scanner-enqueue-all')
def enqueue_all_subreddit_scans():
    """
    Initiates a full scan of the sub-Reddits.
    """
    for subreddit in subreddits.CATALOG.keys():
        worker_url = flask.url_for('sr-scanner-single-scan', subreddit=subreddit)
        taskqueue.add(url=worker_url)
    return "OK"


@app.route('/_workers/sr_scanner/single/<subreddit>',
           endpoint='sr-scanner-single-scan', methods=['POST'])
def scan_subreddit(subreddit):
    """
    Handles the scanning of a single sub-Reddit.
    """
    full_subreddit_scan(subreddit)
    return "OK"
