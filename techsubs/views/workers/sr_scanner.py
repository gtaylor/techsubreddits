import flask
from google.appengine.api import taskqueue

from techsubs import app
from techsubs import subreddits
from techsubs import sr_scanner


@app.route('/_workers/sr_scanner/enqueue-all', endpoint='sr-scanner-enqueue-all')
def enqueue_all_subreddit_scans():
    """
    Initiates a full scan of the sub-Reddits. We enqueue these separately so
    that each scanner worker only hits the Reddit API once, and the task queue
    makes sure only one worker is running at a time. End result is that we stay
    under rate limits.
    """
    for subreddit in subreddits.CATALOG.keys():
        basic_stats = flask.url_for('sr-scanner-basic-stats', subreddit=subreddit)
        taskqueue.add(url=basic_stats)
        post_stats = flask.url_for('sr-scanner-post-stats', subreddit=subreddit)
        taskqueue.add(url=post_stats)
    return "OK"


@app.route('/_workers/sr_scanner/<subreddit>/basic',
           endpoint='sr-scanner-basic-stats', methods=['POST'])
def scan_subreddit_basic_stats(subreddit):
    """
    Scans basic stats about a sub-Reddit. For example, subscriber count
    and currently active users.
    """
    sr_scanner.calc_and_send_basic_subreddit_stats(subreddit)
    return "OK"


@app.route('/_workers/sr_scanner/single/<subreddit>',
           endpoint='sr-scanner-post-stats', methods=['POST'])
def scan_subreddit_post_stats(subreddit):
    """
    Calculates some stats on post activity for a sub-Reddit.
    """
    sr_scanner.calc_and_send_subreddit_post_stats(subreddit)
    return "OK"
