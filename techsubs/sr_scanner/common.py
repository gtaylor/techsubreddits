"""
Logic for scanning sub-Reddits for activity stats.
"""
import json

from google.appengine.api import urlfetch


def send_reddit_api_request(url):
    """
    Use Google App Engine's URL fetch service directly. We only do GET requests,
    so...

    :param str url: The URL to GET.
    :rtype: google.appengine.api.urlfetch._URLFetchResult
    :returns: The fetched result from App Engine's URL fetch service.
    """
    headers = {
        'User-Agent': 'techsubreddits.com by /u/gctaylor',
    }
    result = urlfetch.fetch(url, headers=headers)
    assert result.status_code == 200, "Non-200 status code: %s" % result.status_code
    return result


def get_subreddit_about_dict(subreddit_name):
    """
    :param str subreddit_name: The sub-Reddit to retrieve specifics about.
    :rtype: dict
    :return: A dictionary of details about the sub-Reddit.
    """
    url = 'https://www.reddit.com/r/{}/about.json'.format(subreddit_name)
    result_json = send_reddit_api_request(url).content
    result = json.loads(result_json)
    return result['data']


def get_subreddit_metric_labels(subreddit_name):
    """
    :param str subreddit_name: The sub-Reddit we're sending metrics for.
    :rtype: dict
    :returns: A dict of standard metric labels to send with a data point.
    """
    return {'subreddit': subreddit_name}


