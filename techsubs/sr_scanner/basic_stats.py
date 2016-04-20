"""
This module contains everything needed to calculate some basic, higher-level
stats for a sub-Reddit.
"""
import datetime

from techsubs.metrics.metric_defines import SubRedditSubscribers, \
    SubRedditAccountsActive
from techsubs.sr_scanner.common import get_subreddit_about_dict, \
    get_subreddit_metric_labels


def calc_and_send_basic_subreddit_stats(subreddit_name):
    """
    Calculates and sends some basic stats that we can pull from a sub-Reddit's
    about.json. Unlike :py:func:`calc_and_send_subreddit_post_stats`, this
    reports for the current hour.

    :param subreddit_name: The sub-Reddit to report basic stats for.
    """
    # We can fetch /r/srname/about.json once, then extract a few metrics.
    sr_about = get_subreddit_about_dict(subreddit_name)
    sub_count, accounts_active = _calc_basic_subreddit_stats(sr_about)

    metric_labels = get_subreddit_metric_labels(subreddit_name)
    # time_override is specified so that we can't double-report an hour.
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
