"""
We may need to break this up into multiple modules eventually, but toss any
metrics that we need to track in here.
"""
from techsubs.metrics.common import GaugeMetric


class SubRedditSubscribers(GaugeMetric):
    metric_name = "subreddit.subscribers.count"
    display_name = "Total Subscribers"
    description = "Total number of subscribers per sub-Reddit."
    metric_value_type = 'INT64'

    extra_labels = [
        {
            "key": "subreddit",
            "valueType": "STRING",
            "description": "The sub-Reddit being tracked."
        },
    ]


class SubRedditAccountsActive(GaugeMetric):
    metric_name = "subreddit.accounts.active.count"
    display_name = "Currently Active Accounts"
    description = "Currently Active Accounts per sub-Reddit."
    metric_value_type = 'INT64'

    extra_labels = [
        {
            "key": "subreddit",
            "valueType": "STRING",
            "description": "The sub-Reddit being tracked."
        },
    ]


class SubRedditNewPostCount(GaugeMetric):
    metric_name = "subreddit.posts.new.count"
    display_name = "New Posts"
    description = "Daily totals of new posts per sub-Reddit."
    metric_value_type = 'INT64'

    extra_labels = [
        {
            "key": "subreddit",
            "valueType": "STRING",
            "description": "The sub-Reddit being tracked."
        },
    ]
