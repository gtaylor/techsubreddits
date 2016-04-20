"""
This module contains everything needed to calculate and send stats about
the posts on a sub-Reddit. For example, new posts over time.
"""
import json
import datetime

from techsubs.metrics.metric_defines import SubRedditNewPostCount
from techsubs.sr_scanner.common import get_subreddit_metric_labels, \
    send_reddit_api_request


def calc_and_send_subreddit_post_stats(subreddit_name):
    """
    Calculates and sends hourly post stats for the sub-reddit. This is always
    an hour behind, to make sure that we have the full previous hour's worth
    of posts.

    Assumptions:

    * We run this once per hour. Running this more than once will cause
      the post-related stats to fail, since Google Metrics errors out instead
      of idempotently allowing updates.
    * All of the hour's previous posts are accounted for in the JSON response.
      Keep in mind that un-auth'd requests to /new/.json are cached by
      the CDN for some length of time.

    :param str subreddit_name: The sub-Reddit to make post stats for.
    """
    prev_hour = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
    hour_floor = prev_hour.replace(minute=0, second=0, microsecond=0)
    hour_ceil = prev_hour.replace(minute=59, second=59, microsecond=999999)
    new_posts = _calc_subreddit_post_stats(subreddit_name, hour_floor, hour_ceil)

    metric_labels = get_subreddit_metric_labels(subreddit_name)
    # time_override is specified so that we can't double-report an hour.
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
    result_json = send_reddit_api_request(url).content
    result = json.loads(result_json)
    post_containers = result['data']['children']

    counter = 0
    for post_container in post_containers:
        post = post_container['data']
        post_time = datetime.datetime.utcfromtimestamp(post['created_utc'])
        if start_time <= post_time <= end_time:
            counter += 1
    return counter
