import json
import datetime

import cloudstorage as gcs

from techsubs import subreddits
from techsubs.bucket_populator.common import API_BUCKET_NAME, API_BUCKET_PATH
from techsubs.exceptions import NotFoundError
from techsubs.metrics.metric_defines import SubRedditSubscribers, \
    SubRedditAccountsActive, SubRedditNewPostCount


def generate_and_upload(category):
    overview_json = _generate_json(category)
    uri = '/{bucket_name}/{bucket_path}/category/{category}/overview'.format(
        bucket_name=API_BUCKET_NAME, bucket_path=API_BUCKET_PATH,
        category=category)
    gcs_fobj = gcs.open(
        filename=uri, mode='w',
        content_type='application/json',
        options={'Cache-Control': 'public, max-age=60'})
    gcs_fobj.write(overview_json)
    gcs_fobj.close()


def _generate_json(category):
    if not subreddits.is_valid_subreddit_category(category):
        raise NotFoundError('Invalid Subreddit category.')

    cat_subreddits = subreddits.get_subreddits_in_category(category)
    retval = {
        'generatedTime': datetime.datetime.now().isoformat(),
        'records': [],
        'queryRecordCount': len(cat_subreddits),
        'totalRecordCount': len(cat_subreddits),
    }

    for subreddit in cat_subreddits:
        retval['records'].append(
            _query_and_return_subreddit_stats(subreddit['slug']))
    return json.dumps(retval)


def _query_and_return_subreddit_stats(subreddit_slug):
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(hours=24)
    metric_label_filters = {"subreddit": subreddit_slug}

    subscriber_stats = _query_and_return_subscriber_stats(
        start_time, end_time, metric_label_filters)
    active_accounts_stats = _query_and_return_active_account_stats(
        start_time, end_time, metric_label_filters)
    post_stats = _query_and_return_post_stats(
        start_time, end_time, metric_label_filters)

    return {
        'subreddit': subreddit_slug,
        'accounts_active': active_accounts_stats['24_hour_peak'],
        'new_subscribers': subscriber_stats['24_hour_growth'],
        'total_subscribers': subscriber_stats['current_total'],
        'new_posts': post_stats['24_hour_growth']
    }


def _query_and_return_active_account_stats(start_time, end_time,
                                           metric_label_filters):
    results = SubRedditAccountsActive.query_gauge(
        start_time, end_time, metric_label_filters=metric_label_filters)

    peak_count = 0
    for point in results:
        pval = point['value']
        if pval > peak_count:
            peak_count = pval

    return {
        '24_hour_peak': peak_count,
    }


def _query_and_return_subscriber_stats(start_time, end_time, metric_label_filters):
    results = SubRedditSubscribers.query_gauge(
        start_time, end_time, metric_label_filters=metric_label_filters)

    oldest_point = None
    youngest_point = None
    for point in results:
        ptime = point['time']
        if oldest_point is None or ptime < oldest_point['time']:
            oldest_point = point
        if youngest_point is None or ptime > youngest_point['time']:
            youngest_point = point

    return {
        'current_total': youngest_point['value'],
        '24_hour_growth': youngest_point['value'] - oldest_point['value'],
    }


def _query_and_return_post_stats(start_time, end_time, metric_label_filters):
    results = SubRedditNewPostCount.query_gauge(
        start_time, end_time, metric_label_filters=metric_label_filters)

    total_new = 0
    for point in results:
        total_new += point['value']

    return {
        '24_hour_growth': total_new,
    }
