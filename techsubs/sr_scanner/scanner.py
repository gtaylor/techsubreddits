"""
Logic for scanning sub-Reddits for activity stats.
"""
import json
import datetime

from google.appengine.api import urlfetch

from techsubs.metrics.metric_defines import SubRedditSubscribers, \
    SubRedditNewPostCount, SubRedditAccountsActive


def _send_get_request(url):
    """
    Use Google App Engine's URL fetch service directly. We only do GET requests,
    so...

    :param str url: The URL to GET.
    :rtype: google.appengine.api.urlfetch._URLFetchResult
    :returns: The fetched result from App Engine's URL fetch service.
    """
    result = urlfetch.fetch(url)
    assert result.status_code == 200, "Non-200 status code: %s" % result.status_code
    return result


def _get_subreddit_about(subreddit_name):
    """
    :param str subreddit_name: The sub-Reddit to retrieve specifics about.
    :rtype: dict
    :return: A dictionary of details about the sub-Reddit.
    """
    url = 'https://www.reddit.com/r/{}/about.json'.format(subreddit_name)
    result_json = _send_get_request(url).content
    result = json.loads(result_json)
    return result['data']


def _get_subreddit_metric_labels(subreddit_name):
    """
    :param str subreddit_name: The sub-Reddit we're sending metrics for.
    :rtype: dict
    :returns: A dict of standard metric labels to send with a data point.
    """
    return {'subreddit': subreddit_name}


def full_subreddit_scan(subreddit_name):
    """
    Perform a full scan and report cycle for the given sub-Reddit.

    Assumptions:

    * We run this once per hour.
    * All of the hour's previous posts are accounted for in the JSON response.
      Keep in mind that un-auth'd requests to /new/.json are cached by
      the CDN for some length of time.
    * If we somehow end up running this twice per hour, any existing metrics
      for the hour are over-written with our new values.

    :param str subreddit_name: The sub-Reddit to scan and report metrics for.
    """
    calc_and_send_basic_subreddit_stats(subreddit_name)
    calc_and_send_subreddit_post_stats(subreddit_name)


def calc_and_send_basic_subreddit_stats(subreddit_name):
    """
    Calculates and sends some basic stats that we can pull from a sub-Reddit's
    about.json. Unlike :py:func:`calc_and_send_subreddit_post_stats`, this
    reports for the current hour.

    :param subreddit_name: The sub-Reddit to report basic stats for.
    """
    # We can fetch /r/srname/about.json once, then extract a few metrics.
    sr_about = _get_subreddit_about(subreddit_name)
    sub_count, accounts_active = _calc_basic_subreddit_stats(sr_about)

    metric_labels = _get_subreddit_metric_labels(subreddit_name)
    # We'll lop this down to the first minute of the hour so that we have
    # idempotency.
    hour_floor = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
    SubRedditSubscribers.write_gauge(
        sub_count, labels=metric_labels, time_override=hour_floor)
    SubRedditAccountsActive.write_gauge(
        accounts_active, labels=metric_labels, time_override=hour_floor)


def _calc_basic_subreddit_stats(sr_about):
    """
    :param dict sr_about: An unmarshalled sub-Reddit about.json 'data' dict.
    :rtype: tuple
    :returns: Tuple in the form of: sub_count, accounts_active
    """
    sub_count = int(sr_about['subscribers'])
    accounts_active = int(sr_about['accounts_active'])
    return sub_count, accounts_active


def calc_and_send_subreddit_post_stats(subreddit_name):
    """
    Calculates and sends hourly post stats for the sub-reddit. This is always
    an hour behind, to make sure that we have the full previous hour's worth
    of posts.

    :param str subreddit_name: The sub-Reddit to make post stats for.
    """
    prev_hour = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    hour_floor = prev_hour.replace(minute=0, second=0, microsecond=0)
    hour_ceil = prev_hour.replace(minute=59, second=59, microsecond=999999)
    new_posts = _calc_subreddit_post_stats(subreddit_name, hour_floor, hour_ceil)

    metric_labels = _get_subreddit_metric_labels(subreddit_name)
    # time_override is specified so that we have idempotency.
    SubRedditNewPostCount.write_gauge(
        new_posts, labels=metric_labels, time_override=hour_floor)


def _calc_subreddit_post_stats(subreddit_name, start_time, end_time):
    """
    Calculates some hourly post stats for the sub-reddit. This is always
    an hour behind, to make sure that we have the full hour's worth of posts.

    :param str subreddit_name: The sub-Reddit to make post stats for.
    :param datetime.datetime start_time: Only consider posts that happened after
        this time.
    :param datetime.datetime start_time: Only consider posts that happened before
        this time.
    :rtype: int
    :return: The number of new posts for the given time range.
    """
    url = 'https://www.reddit.com/r/{}/new/.json?limit=100'.format(subreddit_name)
    result_json = _send_get_request(url).content
    result = json.loads(result_json)
    post_containers = result['data']['children']

    counter = 0
    for post_container in post_containers:
        post = post_container['data']
        post_time = datetime.datetime.utcfromtimestamp(post['created_utc'])
        if start_time <= post_time <= end_time:
            counter += 1
    return counter
